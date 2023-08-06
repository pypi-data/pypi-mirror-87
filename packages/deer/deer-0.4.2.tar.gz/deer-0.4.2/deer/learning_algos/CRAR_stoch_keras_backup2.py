"""
Code for the CRAR learning algorithm using Keras

"""

import numpy as np
from keras.optimizers import SGD,RMSprop
from keras import backend as K
from ..base_classes import LearningAlgo
from .NN_CRAR_stoch_keras import NN # Default Neural network used
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
import copy

import matplotlib
matplotlib.use('qt5agg')
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

import random

def mean_squared_error_p(y_true, y_pred):
    """ Modified mean square error that clips
    """
    return K.clip(K.max(  K.square( y_pred - y_true )  ,  axis=-1  )-1,0.,100.)     # = modified mse error L_inf
    #return K.clip(K.mean(  K.square( y_pred - y_true )  ,  axis=-1  )-1,0.,100.)   # = modified mse error L_2

def exp_dec_error(y_true, y_pred):
    return K.exp( - 1* K.sqrt( K.clip(K.sum(K.square(y_pred), axis=-1, keepdims=True),0.000001,10) )  ) # *1 distrib, *5 simple maze

def cosine_proximity2(y_true, y_pred):
    """ This loss is similar to the native cosine_proximity loss from Keras
    but it differs by the fact that only the two first components of the two vectors are used
    """
    y_true = K.l2_normalize(y_true[:,0:2], axis=-1)
    y_pred = K.l2_normalize(y_pred[:,0:2], axis=-1)
    return -K.sum(y_true * y_pred, axis=-1)

#def loss_diff_s_s_(y_true, y_pred):
#    return K.square(   1.    -    K.sqrt(  K.clip( K.sum(y_pred,axis=-1,keepdims=True), 0.000001 , 1. )  )     ) # tend to increase y_pred --> loss -1

class CRAR(LearningAlgo):
    """
    Combined Reinforcement learning via Abstract Representations (CRAR) using Keras
    
    Parameters
    -----------
    environment : object from class Environment
        The environment in which the agent evolves.
    rho : float
        Parameter for rmsprop. Default : 0.9
    rms_epsilon : float
        Parameter for rmsprop. Default : 0.0001
    momentum : float
        Momentum for SGD. Default : 0
    clip_norm : float
        The gradient tensor will be clipped to a maximum L2 norm given by this value.
    freeze_interval : int
        Period during which the target network is freezed and after which the target network is updated. Default : 1000
    batch_size : int
        Number of tuples taken into account for each iteration of gradient descent. Default : 32
    update_rule: str
        {sgd,rmsprop}. Default : rmsprop
    random_state : numpy random number generator
        Set the random seed.
    double_Q : bool, optional
        Activate or not the double_Q learning.
        More informations in : Hado van Hasselt et al. (2015) - Deep Reinforcement Learning with Double Q-learning.
    neural_network : object, optional
        Default is deer.learning_algos.NN_keras
    """

    def __init__(self, environment, rho=0.9, rms_epsilon=0.0001, momentum=0, clip_norm=0, freeze_interval=1000, batch_size=32, update_rule="rmsprop", random_state=np.random.RandomState(), double_Q=False, neural_network=NN, **kwargs):
        """ Initialize the environment
        
        """
        LearningAlgo.__init__(self,environment, batch_size)

        self._rho = rho
        self._rms_epsilon = rms_epsilon
        self._momentum = momentum
        self._clip_norm = clip_norm
        self._update_rule = update_rule
        self._freeze_interval = freeze_interval
        self._double_Q = double_Q
        self._random_state = random_state
        self.update_counter = 0    
        self._high_int_dim = kwargs.get('high_int_dim',False)
        self._internal_dim = kwargs.get('internal_dim',2)
        self.loss_interpret=0
        self.loss_G, self.loss_G2=0, 0
        self.loss_D=0
        self.loss_Q=0
        self.loss_disentangle_t=0
        self.loss_disambiguate1=0
        self.loss_disambiguate2=0
        self.wait_D,self.wait_G=0,0
        
        self.learn_and_plan = neural_network(self._batch_size, self._input_dimensions, self._n_actions, self._random_state, high_int_dim=self._high_int_dim, internal_dim=self._internal_dim)

        self.encoder = self.learn_and_plan.encoder_model()
        self.encoder_diff = self.learn_and_plan.encoder_diff_model(self.encoder)
        
        self.Q = self.learn_and_plan.Q_model()

        self.transition = self.learn_and_plan.transition_model()
        self.transition_d = self.learn_and_plan.transition_discr_model()
        
        self.full_Q=self.learn_and_plan.full_Q_model(self.encoder,self.Q,0,self._df)
                
        # constraint on consecutive t
        self.diff_s_s_ = self.learn_and_plan.encoder_diff_model(self.encoder)
                
        # Grab all the parameters in self.params
        layers=self.encoder.layers+self.Q.layers+self.transition.layers

        self.params = [ param
                    for layer in layers 
                    for param in layer.trainable_weights ]
        #self.params_encoder = [ param
        #            for layer in self.encoder.layers ]
        #            for param in layer.trainable_weights ]


        # Instantiate the same neural network as a target network.
        self.learn_and_plan_target = neural_network(self._batch_size, self._input_dimensions, self._n_actions, self._random_state, high_int_dim=self._high_int_dim, internal_dim=self._internal_dim)
        self.encoder_target = self.learn_and_plan_target.encoder_model()
        self.Q_target = self.learn_and_plan_target.Q_model()
        self.transition_target = self.learn_and_plan_target.transition_model()

        self.full_Q_target = self.learn_and_plan_target.full_Q_model(self.encoder_target,self.Q_target)
        self.full_Q_target.compile(optimizer='rmsprop', loss='mse') #The parameters do not matter since training is done on self.full_Q
        
        self.transition_g_full = self.learn_and_plan.transition_g_full_model(self.encoder, self.transition, self.transition_d)
        self.encoder_g_full = self.learn_and_plan.encoder_g_full_model(self.encoder, self.transition_d)
        self.transition_g_full2 = self.learn_and_plan.transition_g_full_model(self.encoder, self.transition, self.transition_d)

        # Compile all models
        self._compile()

        # Grab all the parameters of the target network together.
        layers_target=self.encoder_target.layers+self.Q_target.layers+self.transition_target.layers

        self.params_target = [ param
                    for layer in layers_target
                    for param in layer.trainable_weights ]
        #self.params_encoder_target = [ param
        #            for layer in self.encoder_target ]
        #            for param in layer.trainable_weights ]

        self._resetQHat()
        #self._updateEncoder()

    def getAllParams(self):
        """ Provides all parameters used by the learning algorithm

        Returns
        -------
        Values of the parameters: list of numpy arrays
        """
        params_value=[]
        for i,p in enumerate(self.params):
            params_value.append(K.get_value(p))
        return params_value

    def setAllParams(self, list_of_values):
        """ Set all parameters used by the learning algorithm

        Arguments
        ---------
        list_of_values : list of numpy arrays
             list of the parameters to be set (same order than given by getAllParams()).
        """
        for i,p in enumerate(self.params):
            K.set_value(p,list_of_values[i])

    def train(self, states_val, actions_val, rewards_val, next_states_val, terminals_val):
        """
        Train CRAR from one batch of data.

        Parameters
        -----------
        states_val : numpy array of objects
            Each object is a numpy array that relates to one of the observations
            with size [batch_size * history size * size of punctual observation (which is 2D,1D or scalar)]).
        actions_val : numpy array of integers with size [self._batch_size]
            actions[i] is the action taken after having observed states[:][i].
        rewards_val : numpy array of floats with size [self._batch_size]
            rewards[i] is the reward obtained for taking actions[i-1].
        next_states_val : numpy array of objects
            Each object is a numpy array that relates to one of the observations
            with size [batch_size * history size * size of punctual observation (which is 2D,1D or scalar)]).
        terminals_val : numpy array of booleans with size [self._batch_size]
            terminals[i] is True if the transition leads to a terminal state and False otherwise

        Returns
        -------
        Average loss of the batch training for the Q-values (RMSE)
        Individual (square) losses for the Q-values for each tuple
        """
        
        onehot_actions = np.zeros((self._batch_size, self._n_actions))
        onehot_actions[np.arange(self._batch_size), actions_val] = 1
        onehot_actions_rand = np.zeros((self._batch_size, self._n_actions))
        onehot_actions_rand[np.arange(self._batch_size), np.random.randint(0,2,(32))] = 1
        states_val=list(states_val)
        next_states_val=list(next_states_val)
        terminals_val = terminals_val.astype('float')
            
        Es_=self.encoder.predict(next_states_val)#self.encoder_target.predict(next_states_val)
        Es=self.encoder.predict(states_val)
        
        noise = np.random.normal(0, 1, Es.shape)

        ETs, R, terminals=self.transition.predict([Es,onehot_actions,noise])
                   
        if(self.update_counter%2000==0):
            print ("Printing a few elements useful for debugging:")
            #print ("states_val[0][0]")
            #print (states_val[0][0])
            #print ("next_states_val[0][0]")
            #print (next_states_val[0][0])
            print ("actions_val[0], rewards_val[0], terminals_val[0]")
            print (actions_val[0], rewards_val[0], terminals_val[0])
            print ("Es[0],ETs[0],Es_[0]")
            if(Es.ndim==4):
                print (np.transpose(Es, (0, 3, 1, 2))[0],np.transpose(ETs, (0, 3, 1, 2))[0],np.transpose(Es_, (0, 3, 1, 2))[0])    # data_format='channels_last' --> 'channels_first'
            else:
                print (Es[0],ETs[0],Es_[0])

            if (self._high_int_dim==True):
                #fig = plt.figure()
                plt.subplot(2,3,1)
                if(len(states_val[0][0,0].shape)==2):
                    plt.imshow(states_val[0][0,0].astype('float32'))
                if(len(states_val[0][0,0].shape)==3):
                    plt.imshow(states_val[0][0,0,0].astype('float32'))
                plt.subplot(2,3,4)
                plt.imshow(Es[0])
                plt.subplot(2,3,5)
                plt.imshow(ETs[0])
                plt.subplot(2,3,3)
                if(len(states_val[0][0,0].shape)==2):
                    plt.imshow(next_states_val[0][0,0].astype('float32'))
                if(len(states_val[0][0,0].shape)==3):
                    plt.imshow(next_states_val[0][0,0,0].astype('float32') )
                plt.subplot(2,3,6)
                plt.imshow(Es_[0])
                plt.show()
                plt.savefig('plot9.pdf')
                print("here")
                print ("R[0],terminals[0]")
                print (R[0],terminals[0])
                
        
        noise_level=max( (1.-self.update_counter/50000) , 0.1 ) #0.2
        
        
        # Fit the transition discriminator
        # First half of the transitions are "True" and the other half is generated.
        true_transitions=np.concatenate(  ( np.ones((self._batch_size//2,1)) , np.zeros((self._batch_size//2,1)) )  ,  axis=0  )
        Es_[self._batch_size//2:]=ETs[self._batch_size//2:]
        Es_[:self._batch_size//2]+=np.random.normal(0,noise_level/2.,Es_[:self._batch_size//2].shape)
        rewards_val[self._batch_size//2:]=R[self._batch_size//2:,0]
        rewards_val[:self._batch_size//2]+=np.random.normal(0,noise_level/2.,(self._batch_size//2))
        terminals_val[self._batch_size//2:]=terminals[self._batch_size//2:,0]
        terminals_val[:self._batch_size//2]+=np.random.normal(0,noise_level/2.,(self._batch_size//2))
        Es__noise=Es_#+np.random.normal(0,0.05,Es_.shape)
        rewards_val_noise=rewards_val#+np.random.normal(0,0.2,rewards_val.shape)
        terminals_val_noise=terminals_val#+np.random.normal(0,0.2,terminals_val.shape)
        
        if (self.wait_D==0):
            self.loss_D=0.95*self.loss_D+0.05*self.transition_d.train_on_batch([Es,onehot_actions,Es__noise,rewards_val_noise,terminals_val_noise], true_transitions )
            #if(self.loss_D<0.4 and self.loss_G>1.2):
            #    self.wait_D=4
            #if(self.loss_D<0.2 and self.loss_G>2.):
            #    self.wait_D=4
            #elif(self.loss_D<0.1 and self.loss_G>3.):
            #    self.wait_D=16
        else:
            self.wait_D-=1
            #print ( self.transition_d.predict([Es,onehot_actions,Es_,rewards_val,terminals_val]) )
            #print ([Es,onehot_actions,Es_,rewards_val,terminals_val])
            #print ( true_transitions )
            #print ("self.loss_D")
            #print (self.loss_D)
        
        # Fit transition and encoder by trying to fool the discriminator
        if (self.wait_G==0):
            self.loss_G=0.95*self.loss_G+0.05*self.transition_g_full.train_on_batch(states_val+[onehot_actions,noise], np.ones((self._batch_size,1)) )
            self.loss_G2=0.95*self.loss_G2+0.05*self.encoder_g_full.train_on_batch(states_val+[onehot_actions]+next_states_val+[rewards_val,terminals_val,np.random.normal(0,noise_level/2.,Es_[:self._batch_size].shape), np.random.normal(0,noise_level/2.,(self._batch_size)), np.random.normal(0,noise_level/2.,(self._batch_size))], np.zeros((self._batch_size,1)) )
            self.transition_g_full2.train_on_batch(states_val+[onehot_actions,noise], np.ones((self._batch_size,1)) )
            #if(self.loss_G<0.4 and self.loss_D>1.2):
            #    self.wait_G=4
            #if(self.loss_G<0.2 and self.loss_D>2.):
            #    self.wait_G=4
            #elif(self.loss_G<0.1 and self.loss_D>3.):
            #    self.wait_G=16
        else:
            self.wait_G-=1
            #print ("self.loss_G")
            #print (self.loss_G)
            
        
        # Loss to ensure entropy but limited volume in abstract state space, avg=0 and sigma=1
        # reduce the squared value of the abstract features
        self.loss_disambiguate1+=self.encoder.train_on_batch(states_val,np.zeros_like(Es)) #np.zeros((self._batch_size,self.learn_and_plan.internal_dim)))

        # Increase the entropy in the abstract features of two states
        # This works only when states_val is made up of only one observation --> FIXME
        rolled=np.roll(states_val[0],1,axis=0)
        self.loss_disambiguate2+=self.encoder_diff.train_on_batch([states_val[0],rolled],np.reshape(np.zeros_like(Es),(self._batch_size,-1)))

        self.loss_disentangle_t+=self.diff_s_s_.train_on_batch(states_val+next_states_val, np.reshape(np.zeros_like(Es),(self._batch_size,-1)))

        # Interpretable AI
        if(self._high_int_dim==False):
            target_modif_features=np.zeros((self._n_actions,self._internal_dim))
            ## Catcher
            #target_modif_features[0,0]=1    # dir
            #target_modif_features[1,0]=-1   # opposite dir
            #target_modif_features[0:2,1]=1    # temps
            ## Laby
            target_modif_features[0,0]=1
            target_modif_features[1,0]=0
            #target_modif_features[2,1]=0
            #target_modif_features[3,1]=0
            target_modif_features=np.repeat(target_modif_features,self._batch_size,axis=0)
            states_val_tiled=[]
            for obs in states_val:
                states_val_tiled.append(np.tile(obs,(self._n_actions,1,1,1)))
            onehot_actions_tiled = np.diag(np.ones(self._n_actions))#np.zeros((self._batch_size*self._n_actions, self._n_actions))
            onehot_actions_tiled = np.repeat(onehot_actions_tiled,self._batch_size,axis=0)
                
        
        if(self.update_counter%2000==0):
            print ("self.loss_G, self.loss_D, self.loss_Q/500., self.loss_disentangle_t/500., self.loss_disambiguate1/500., self.loss_disambiguate2/500.")
            print (self.loss_G, self.loss_D, self.loss_Q/500., self.loss_disentangle_t/500., self.loss_disambiguate1/500., self.loss_disambiguate2/500.)

            if(self._high_int_dim==False):
                print ("self.loss_interpret/500.")
                print (self.loss_interpret/500.)

            #self.loss_G=0
            #self.loss_D=0
            self.loss_Q=0
            self.loss_interpret=0

            self.loss_disentangle_t=0
            self.loss_disambiguate1=0
            self.loss_disambiguate2=0

        if self.update_counter % self._freeze_interval == 0:
            self._resetQHat()
            #self._updateEncoder()
        
        next_q_vals = self.full_Q_target.predict(next_states_val)
        
        if(self._double_Q==True):
            next_q_vals_current_qnet=self.full_Q.predict(next_states_val)
            argmax_next_q_vals=np.argmax(next_q_vals_current_qnet, axis=1)
            max_next_q_vals=next_q_vals[np.arange(self._batch_size),argmax_next_q_vals].reshape((-1, 1))
        else:
            max_next_q_vals=np.max(next_q_vals, axis=1, keepdims=True)

        not_terminals=np.ones_like(terminals_val,dtype=float) - terminals_val
        
        target = rewards_val + not_terminals * self._df * max_next_q_vals.reshape((-1))
        
        q_vals=self.full_Q.predict([states_val[0]])
        
        # In order to obtain the individual losses, we predict the current Q_vals and calculate the diff
        q_val=q_vals[np.arange(self._batch_size), actions_val]#.reshape((-1, 1))        
        diff = - q_val + target 
        loss_ind=pow(diff,2)
                
        q_vals[  np.arange(self._batch_size), actions_val  ] = target
                
        # Is it possible to use something more flexible than this? 
        # Only some elements of next_q_vals are actual value that I target. 
        # My loss should only take these into account.
        # Workaround here is that many values are already "exact" in this update

        loss=0
        loss=self.full_Q.train_on_batch(states_val , q_vals ) 
        self.loss_Q+=loss

        if(self.update_counter%100==0):
            print ("Number of training steps:"+str(self.update_counter)+".")
        
        self.update_counter += 1        

        return np.sqrt(loss),loss_ind


    def qValues(self, state_val):
        """ Get the q values for one pseudo-state (without planning)

        Arguments
        ---------
        state_val : array of objects (or list of objects)
            Each object is a numpy array that relates to one of the observations
            with size [1 * history size * size of punctual observation (which is 2D,1D or scalar)]).

        Returns
        -------
        The q values for the provided pseudo state
        """ 
        copy_state=copy.deepcopy(state_val) #Required!

        return self.full_Q.predict([np.expand_dims(state,axis=0) for state in copy_state])[0]

    def qValues_planning(self, state_val, transition, Q, d=5):
        """ Get the average Q-values up to planning depth d for one pseudo-state.
        
        Arguments
        ---------
        state_val : array of objects (or list of objects)
            Each object is a numpy array that relates to one of the observations
            with size [1 * history size * size of punctual observation (which is 2D,1D or scalar)]).
        transition : transition_model
            Model that fits the transition between abstract representation
        Q : Q_model
            Model that fits the optimal Q-value
        d : int
            planning depth

        Returns
        -------
        The average q values with planning depth up to d for the provided pseudo-state
        """
        encoded_x = self.encoder.predict(state_val)

#        ## DEBUG PURPOSES
#        print ( "self.full_Q.predict(state_val)[0]" )
#        print ( self.full_Q.predict(state_val)[0] )
#        identity_matrix = np.diag(np.ones(self._n_actions))
#        if(encoded_x.ndim==2):
#            tile3_encoded_x=np.tile(encoded_x,(self._n_actions,1))
#        elif(encoded_x.ndim==4):
#            tile3_encoded_x=np.tile(encoded_x,(self._n_actions,1,1,1))
#        else:
#            print ("error")
#        
#        repeat_identity=np.repeat(identity_matrix,len(encoded_x),axis=0)
#        ##print tile3_encoded_x
#        ##print repeat_identity
#        r_vals_d0=np.array(R.predict([tile3_encoded_x,repeat_identity]))
#        #print "r_vals_d0"
#        #print r_vals_d0
#        r_vals_d0=r_vals_d0.flatten()
#        print "r_vals_d0"
#        print r_vals_d0
#        next_x_predicted=T.predict([tile3_encoded_x,repeat_identity])
#        #print "next_x_predicted"
#        #print next_x_predicted
#        one_hot_first_action=np.zeros((1,self._n_actions))
#        one_hot_first_action[0]=1
#        next_x_predicted=T.predict([next_x_predicted[0:1],one_hot_first_action])
#        next_x_predicted=T.predict([next_x_predicted[0:1],one_hot_first_action])
#        next_x_predicted=T.predict([next_x_predicted[0:1],one_hot_first_action])
#        #print "next_x_predicted action 0 t4"
#        #print next_x_predicted
#        ## END DEBUG PURPOSES

        QD_plan=0
        for i in range(d+1):
            Qd=self.qValues_planning_abstr(encoded_x, transition, Q, d=i, branching_factor=[self._n_actions,2,2,2,2,2,2,2], repeat_factor=[5,4,3,3,3,3,3,3]).reshape(len(encoded_x),-1)
            #print ("Qd,i")
            #print (Qd,i)
            QD_plan+=Qd
        QD_plan=QD_plan/(d+1)
        
        print ("QD_plan")
        print (QD_plan)

        return QD_plan
  
    def qValues_planning_abstr(self, state_abstr_val, transition, Q, d, branching_factor=None, repeat_factor=None):
        """ Get the q values for pseudo-state(s) with a planning depth d. 
        This function is called recursively by decreasing the depth d at every step.

        Arguments
        ---------
        state_abstr_val : internal state(s).
        transition : transition_model
            Model that fits the transition between abstract representation
        Q : Q_model
            Model that fits the optimal Q-value
        d : int
            planning depth

        Returns
        -------
        The Q-values with planning depth d for the provided encoded state(s)
        """
        # !! We require that the first branching factor is self._n_actions so that this function return values 
        # with the right dimension (=self._n_actions). 
                
        identity_matrix = np.identity(self._n_actions)
        
        this_branching_factor=branching_factor.pop(0)
        this_repeat_factor=repeat_factor.pop(0)
                         
        #if(state_abstr_val.ndim==2):
        #    tile3_encoded_x=np.repeat(state_abstr_val,this_repeat_factor,axis=0)
        #elif(state_abstr_val.ndim==4):
        #tile3_encoded_x=np.repeat(state_abstr_val,this_repeat_factor,axis=0)
        
        #print ("state_abstr_val[:5]")
        #print (state_abstr_val[:5])
        #q_values_reshaped=Q.predict([tile3_encoded_x]).reshape(len(state_abstr_val),this_repeat_factor,self._n_actions)            
        #print (q_values_reshaped[:5])
        #mean_q_values=np.mean(q_values_reshaped,axis=1).reshape(len(state_abstr_val),self._n_actions)
        #print (mean_q_values[:5])
        #Q.predict([state_abstr_val]) # ?TO REMOVE? because now corresponds to mean_q_values
        q_values=Q.predict(state_abstr_val) #np.zeros((len(state_abstr_val),self._n_actions)) #Q.predict(state_abstr_val)
        #print ("q_values[:5]")
        #print (q_values[:5])
        
        
        if (d==0):   
            # At the leaf of the planning tree, the function        
            # returns the estimated Q-values (without recurrent call to this function)         
            if(this_branching_factor<self._n_actions):
                return np.partition(q_values, -this_branching_factor)[:,-this_branching_factor:]
            else:
                return q_values # no change in the order of the actions
        else:
            # If not at the leaf of the planning tree, the function           
            # returns the estimated Q-values (with recurrent call to this function)         
            tile3_encoded_x=np.repeat(state_abstr_val,this_branching_factor*this_repeat_factor,axis=0)
            if(this_branching_factor==self._n_actions):
                # All actions are considered in the tree
                # NB: For this case, we do not use argpartition because we want to keep the actions in the natural order
                # That way, this function returns the Q-values for all actions with planning depth d in the right order
                repeat_identity=np.repeat(identity_matrix,len(state_abstr_val)*this_repeat_factor,axis=0)
            else:
                # A subset of the actions corresponding to the best estimated Q-values are considered at each branch 
                estim_Q_values=q_values #Q.predict([state_abstr_val])
                ind = np.argpartition(estim_Q_values, -this_branching_factor)[:,-this_branching_factor:]
                #print ("ind[:5]")
                #print (ind[:5])
                ind_r = np.repeat(ind,this_repeat_factor,axis=0)
                #print ("ind_r[:5]")
                #print (ind_r[:5])
                #print (ind.shape,ind_r.shape)
                # Replacing ind if we want random branching
                #ind = np.random.randint(0,self._n_actions,size=ind.shape)
                repeat_identity=identity_matrix[ind_r].reshape(len(state_abstr_val)*this_branching_factor*this_repeat_factor,self._n_actions)
                #print (repeat_identity[:5])
            
            noise=np.random.normal(0, 1, tile3_encoded_x.shape) #FIXME to avoid hard code of 0 and 1 ?
            #print ("tile3_encoded_x.shape,repeat_identity.shape,noise.shape")
            #print (tile3_encoded_x.shape,repeat_identity.shape,noise.shape)
            next_x_predicted, r_vals_d0, terminal_vals_d0=transition.predict([tile3_encoded_x,repeat_identity,noise])
            #print ("next_x_predicted.shape,r_vals_d0.shape,noise.shape")
            #print (next_x_predicted.shape,r_vals_d0.shape,terminal_vals_d0.shape)
            gamma_vals_d0=(1-terminal_vals_d0)*0.9 #FIXME hard-coded value
            
            #r_vals_d0=np.array(R.predict([tile3_encoded_x,repeat_identity]))
            r_vals_d0=r_vals_d0.flatten()
            #r_vals_d0=r_vals_d0.reshape(-1,repeat_factor[0])
            #r_vals_d0=np.mean(r_vals_d0,axis=1).flatten()
            
            #gamma_vals_d0=np.array(gamma.predict([tile3_encoded_x,repeat_identity]))
            gamma_vals_d0=gamma_vals_d0.flatten()
            #gamma_vals_d0=gamma_vals_d0.reshape(-1,repeat_factor[0])
            #gamma_vals_d0=np.mean(gamma_vals_d0,axis=1).flatten()

            #next_x_predicted=T.predict([tile3_encoded_x,repeat_identity])
            
            q_values=self.qValues_planning_abstr(next_x_predicted,transition,Q,d=d-1,branching_factor=branching_factor,repeat_factor=repeat_factor)
            #print("q_values.shape")
            #print(q_values.shape)
            q_values=r_vals_d0+gamma_vals_d0*np.max(q_values,axis=1).flatten()
            
            #print(q_values.shape)
            
            q_values_reshaped=q_values.reshape(len(state_abstr_val)*this_branching_factor,this_repeat_factor)#*this_repeat_factor,repeat_factor[0])            
            mean_q_values=np.mean(q_values_reshaped,axis=1).reshape(len(state_abstr_val),this_branching_factor)#flatten()
            #print(mean_q_values.shape)
            
            #mean_q_values_reshaped=mean_q_values.reshape(len(state_abstr_val)*this_branching_factor,branching_factor[0])
            #max_mean_q_values=np.amax(mean_q_values_reshaped,axis=1).flatten()
            
            return mean_q_values

    def chooseBestAction(self, state, mode, *args, **kwargs):
        """ Get the best action for a pseudo-state

        Arguments
        ---------
        state : list of numpy arrays
             One pseudo-state. The number of arrays and their dimensions matches self.environment.inputDimensions().
        mode : int
            Identifier of the mode (-1 is reserved for the training mode).

        Returns
        -------
        The best action : int
        """
        copy_state=copy.deepcopy(state) #Required because of the "hack" below

        if(mode==None):
            mode=0
        di=[0,1,3,6]
        # We use the mode to define the planning depth
        q_vals = self.qValues_planning([np.expand_dims(s,axis=0) for s in copy_state], self.transition, self.Q, d=di[mode])

        return np.argmax(q_vals),np.max(q_vals)
        
    def _compile(self):
        """ Compile all the optimizers for the different losses
        """
        if (self._update_rule=="sgd"):
            optimizer=SGD(lr=self._lr, momentum=self._momentum, nesterov=False, clipvalue=self._clip_norm)
            optimizer1=SGD(lr=self._lr, momentum=self._momentum, nesterov=False, clipvalue=self._clip_norm) # Different optimizers for each network; 
            optimizer2=SGD(lr=self._lr, momentum=self._momentum, nesterov=False, clipvalue=self._clip_norm) # to possibly modify them separately
            optimizer4=SGD(lr=self._lr, momentum=self._momentum, nesterov=False, clipvalue=self._clip_norm)
            optimizer5=SGD(lr=self._lr, momentum=self._momentum, nesterov=False, clipvalue=self._clip_norm)
            optimizer6=SGD(lr=self._lr, momentum=self._momentum, nesterov=False, clipvalue=self._clip_norm)
            optimizer7=SGD(lr=self._lr, momentum=self._momentum, nesterov=False, clipvalue=self._clip_norm)
        elif (self._update_rule=="rmsprop"):
            optimizer=RMSprop(lr=self._lr, rho=self._rho, epsilon=self._rms_epsilon, clipvalue=self._clip_norm)
            optimizer1=RMSprop(lr=self._lr, rho=self._rho, epsilon=self._rms_epsilon, clipvalue=self._clip_norm) # Different optimizers for each network; 
            optimizer2=RMSprop(lr=self._lr, rho=self._rho, epsilon=self._rms_epsilon, clipvalue=self._clip_norm) # to possibly modify them separately
            optimizer2b=RMSprop(lr=self._lr, rho=self._rho, epsilon=self._rms_epsilon, clipvalue=self._clip_norm) # to possibly modify them separately
            optimizer3=RMSprop(lr=self._lr, rho=self._rho, epsilon=self._rms_epsilon, clipvalue=self._clip_norm) # to possibly modify them separately
            optimizer4=RMSprop(lr=self._lr, rho=self._rho, epsilon=self._rms_epsilon, clipvalue=self._clip_norm)
            optimizer5=RMSprop(lr=self._lr, rho=self._rho, epsilon=self._rms_epsilon, clipvalue=self._clip_norm)
            optimizer6=RMSprop(lr=self._lr, rho=self._rho, epsilon=self._rms_epsilon, clipvalue=self._clip_norm)
            optimizer7=RMSprop(lr=self._lr, rho=self._rho, epsilon=self._rms_epsilon, clipvalue=self._clip_norm)

        else:
            raise Exception('The update_rule '+self._update_rule+' is not implemented.')
        
        self.encoder.trainable = False
        self.encoder_target.trainable = False
        self.full_Q.compile(optimizer=optimizer, loss='mse')

        self.transition_d.compile(optimizer=optimizer1,
                  loss='binary_crossentropy')

        self.transition_d.trainable = False
        self.transition_g_full2.compile(optimizer=optimizer2,
                  loss='binary_crossentropy') # transition are updated, encoder + encoder_target are not

        self.encoder_target.trainable = True
        self.encoder_g_full.compile(optimizer=optimizer3,
                  loss='binary_crossentropy') # encoder_target is updated
        self.encoder.trainable = True

        self.transition_g_full.compile(optimizer=optimizer3,
                  loss='binary_crossentropy') # encoder +transition are updated, encoder_target is not

        self.transition_d.trainable = True

        self.encoder.compile(optimizer=optimizer4,
                  loss=mean_squared_error_p)
        self.encoder_diff.compile(optimizer=optimizer5,
                  loss=exp_dec_error)

        self.diff_s_s_.compile(optimizer=optimizer6,
                  loss=exp_dec_error)
        

    def _resetQHat(self):
        """ Set the target Q-network weights equal to the main Q-network weights
        """
        for i,(param,next_param) in enumerate(zip(self.params, self.params_target)):
            #new_vals=K.get_value(param)/2.+K.get_value(next_param)/2.
            #K.set_value(next_param,new_vals)
            K.set_value(next_param,K.get_value(param))

    #def _updateEncoder(self):
    #    """ Set the target Q-network weights equal to the main Q-network weights
    #    """
    #    for i,(param,next_param) in enumerate(zip(self.params_encoder, self.params_encoder_target)):
    #        K.set_value(next_param,K.get_value(param))

    def setLearningRate(self, lr):
        """ Setting the learning rate

        Parameters
        -----------
        lr : float
            The learning rate that has to be set
        """
        self._lr = lr
        print ("New learning rate set to "+str(self._lr)+".")
        # Changing the learning rates (NB:recompiling seems to lead to memory leaks!)
        K.set_value(self.full_Q.optimizer.lr, self._lr)

        K.set_value(self.transition_d.optimizer.lr, self._lr)
        K.set_value(self.transition_g_full.optimizer.lr, self._lr/10.) # /1. for simple laby or simple catcher; /10. for distrib of laby
        K.set_value(self.encoder_g_full.optimizer.lr, self._lr/10.) # /1. for simple laby or simple catcher; /10. or distrib of laby
        K.set_value(self.transition_g_full2.optimizer.lr, self._lr)
        
        K.set_value(self.encoder.optimizer.lr, self._lr)
        K.set_value(self.encoder_diff.optimizer.lr, self._lr*5) # *1. for simple laby or simple catcher; *5 for distrib of laby

        K.set_value(self.diff_s_s_.optimizer.lr, self._lr/1.) # /5. for simple laby or simple catcher; /1. for distrib of laby

    def transfer(self, original, transfer, epochs=1):
        # First, make sure that the target network and the current network are the same
        self._resetQHat()
        # modify the loss of the encoder
        optimizer4=RMSprop(lr=self._lr, rho=0.9, epsilon=1e-06)
        self.encoder.compile(optimizer=optimizer4, loss='mse')
        
        # Then, train the encoder such that the original and transfer states are mapped into the same abstract representation
        x_original=self.encoder.predict(original)#[0]
        print ("x_original[0:10]")
        print (x_original[0:10])
        for i in range(epochs):
            size = original[0].shape[0]
            print ( "train" )
            print ( self.encoder.train_on_batch(transfer[0][0:int(size*0.8)] , x_original[0:int(size*0.8)] ) )
            print ( "validation" )
            print ( self.encoder.test_on_batch(transfer[0][int(size*0.8):] , x_original[int(size*0.8):]) )
         
        self.encoder.compile(optimizer=optimizer4,
                  loss=mean_squared_error_p)

