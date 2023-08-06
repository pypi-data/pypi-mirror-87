"""
CRAR Neural network using Keras

"""

import numpy as np
from keras import backend as K
from keras.models import Model
from keras.layers import Input, Layer, Dense, Flatten, Activation, Conv2D, MaxPooling2D, UpSampling2D, Reshape, Permute, Add, Subtract, Dot, Multiply, Average, Lambda, Concatenate, BatchNormalization, merge, RepeatVector, AveragePooling2D, Dropout
from keras import regularizers
#np.random.seed(111111)
import math

class NN():
    """
    Deep Q-learning network using Keras
    
    Parameters
    -----------
    batch_size : int
        Number of tuples taken into account for each iteration of gradient descent
    input_dimensions :
    n_actions :
    random_state : numpy random number generator
    high_int_dim : Boolean
        Whether the abstract state should be high dimensional in the form of frames/vectors or whether it should 
        be low-dimensional
    """
    def __init__(self, batch_size, input_dimensions, n_actions, random_state, **kwargs):
        self._input_dimensions=input_dimensions
        dim=self._input_dimensions[0] #FIXME        
        self._pooling_encoder = 6 # We consider for frames and stack of frames a pooling of 4 in the encoder
        self.n_rows = math.ceil(dim[-2] / self._pooling_encoder)
        self.n_cols = math.ceil(dim[-1] / self._pooling_encoder)

        self._batch_size=batch_size
        self._random_state=random_state
        self._n_actions=n_actions
        self._high_int_dim=kwargs["high_int_dim"]
        if(self._high_int_dim==True):
            self.n_channels_internal_dim=kwargs["internal_dim"] #dim[-3]
        else:
            self.internal_dim=kwargs["internal_dim"]    #2 for laby
                                                        #3 for catcher

    def encoder_model(self):
        """ Instantiate a Keras model for the encoder of the CRAR learning algorithm.
        
        The model takes the following as input 
        s : list of objects
            Each object is a numpy array that relates to one of the observations
            with size [batch_size * history size * size of punctual observation (which is 2D,1D or scalar)]).
        
        Parameters
        -----------
        
    
        Returns
        -------
        Keras model with output x (= encoding of s)
    
        """
        outs_conv=[]
        inputs=[]

        for i, dim in enumerate(self._input_dimensions):
            # - observation[i] is a FRAME
            if len(dim) == 3 or len(dim) == 4:
                if(len(dim) == 4):
                    input = Input(shape=(dim[-4],dim[-3],dim[-2],dim[-1]))
                    inputs.append(input)
                    input = Reshape((dim[-4]*dim[-3],dim[-2],dim[-1]), input_shape=(dim[-4],dim[-3],dim[-2],dim[-1]))(input)
                    x=Permute((2,3,1), input_shape=(dim[-4]*dim[-3],dim[-2],dim[-1]))(input)    #data_format='channels_last'
                else:
                    input = Input(shape=(dim[-3],dim[-2],dim[-1]))
                    inputs.append(input)
                    x=Permute((2,3,1), input_shape=(dim[-3],dim[-2],dim[-1]))(input)    #data_format='channels_last'

                if(dim[-2]>12 and dim[-1]>12):
                    x = Conv2D(8, (2, 2), padding='same', activation='tanh')(x)
                    x = Conv2D(16, (2, 2), padding='same', activation='tanh')(x)
                    #x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
                    x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(x)
                    x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
                    #x = MaxPooling2D(pool_size=(3, 3), strides=None, padding='same')(x)
                    x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
                    x = MaxPooling2D(pool_size=(3, 3), strides=None, padding='same')(x)
                    #x = Conv2D(8, (2, 2), padding='same', activation='tanh')(x)
                    #x = Conv2D(16, (2, 2), padding='same', activation='tanh')(x)
                    ##x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
                    #x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(x)
                    #x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
                    #x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(x)
                    #x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
                    #x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(x)

                #else:
                #    print ("FIXME")
                #    #self._pooling_encoder=1
                    
                if(self._high_int_dim==True):
                    x = Conv2D(self.n_channels_internal_dim, (1, 1), padding='same')(x) #, activation='tanh'
                    out = x
                else:
                    out = Flatten()(x)
                
            # - observation[i] is a VECTOR
            elif len(dim) == 2:
                if dim[-3] > 3:
                    input = Input(shape=(dim[-3],dim[-2]))
                    inputs.append(input)
                    reshaped=Reshape((dim[-3],dim[-2],1), input_shape=(dim[-3],dim[-2]))(input)     #data_format='channels_last'
                    x = Conv2D(16, (2, 1), activation='tanh', border_mode='valid')(reshaped)    #Conv on the history
                    x = Conv2D(16, (2, 2), activation='tanh', border_mode='valid')(x)           #Conv on the history & features
            
                    if(self._high_int_dim==True):
                        out = x
                    else:
                        out = Flatten()(x)
                else:
                    input = Input(shape=(dim[-3],dim[-2]))
                    inputs.append(input)
                    out = Flatten()(input)
            
            # - observation[i] is a SCALAR -
            else:
                if dim[-3] > 3:
                    # this returns a tensor
                    input = Input(shape=(dim[-3],))
                    inputs.append(input)
                    reshaped=Reshape((1,dim[-3],1), input_shape=(dim[-3],))(input)            #data_format='channels_last'
                    x = Conv2D(8, (1,2), activation='tanh', border_mode='valid')(reshaped)  #Conv on the history
                    x = Conv2D(8, (1,2), activation='tanh', border_mode='valid')(x)         #Conv on the history
                    
                    if(self._high_int_dim==True):
                        out = x
                    else:
                        out = Flatten()(x)
                                        
                else:
                    input = Input(shape=(dim[-3],))
                    inputs.append(input)
                    out=input
                    
            outs_conv.append(out)
        
        if(self._high_int_dim==True):
            model = Model(inputs=inputs, outputs=outs_conv)

        if(self._high_int_dim==False):
            if len(outs_conv)>1:
                x = merge(outs_conv, mode='concat')
            else:
                x= outs_conv [0]
        
            # we stack a deep fully-connected network on top
            x = Dense(200, activation='tanh')(x)
            x = Dense(100, activation='tanh')(x)
            x = Dense(50, activation='tanh')(x)
            x = Dense(10, activation='tanh')(x)
        
            x = Dense(self.internal_dim)(x)#, activity_regularizer=regularizers.l2(0.00001))(x) #, activation='tanh'
        
            model = Model(inputs=inputs, outputs=x)
        
        return model

    def encoder_diff_model(self,encoder_model):
        """ Instantiate a Keras model that provides the difference between two encoded pseudo-states
        
        The model takes the two following inputs:
        s1 : list of objects
            Each object is a numpy array that relates to one of the observations
            with size [batch_size * history size * size of punctual observation (which is 2D,1D or scalar)]).
        s2 : list of objects
            Each object is a numpy array that relates to one of the observations
            with size [batch_size * history size * size of punctual observation (which is 2D,1D or scalar)]).
        
        Parameters
        -----------
        encoder_model: instantiation of a Keras model for the encoder
    
        Returns
        -------
        model with output the difference between the encoding of s1 and the encoding of s2
    
        """
        inputs=[]
        
        for j in range(2):
            for i, dim in enumerate(self._input_dimensions):
                if(len(dim) == 4):
                    input = Input(shape=(dim[-4],dim[-3],dim[-2],dim[-1]))
                    inputs.append(input)
                    input = Reshape((dim[-4]*dim[-3],dim[-2],dim[-1]), input_shape=(dim[-4],dim[-3],dim[-2],dim[-1]))(input)
                elif(len(dim) == 3):
                    input = Input(shape=(dim[-3],dim[-2],dim[-1]))
                    inputs.append(input)
                elif len(dim) == 2:
                    input = Input(shape=(dim[-3],dim[-2]))
                    inputs.append(input)
                else:
                    input = Input(shape=(dim[-3],))
                    inputs.append(input)
        
        half = len(inputs)//2
        x1 = encoder_model(inputs[:half])
        x2 = encoder_model(inputs[half:])
        
        if (self._high_int_dim==True):
            x1=Flatten()(x1)
            x2=Flatten()(x2)
        x = Subtract()([x1,x2])
        model = Model(inputs=inputs, outputs=x)
        
        return model

    def discrim_masked_full_model(self,encoder_model,encoder_frozen_model,transition_model,discrim_masked_model,plan_depth=0):
        """ 
        For plan_depth=0, the model takes the four following inputs:
        s1 : list of objects
            Each object is a numpy array that relates to one of the observations
            with size [batch_size * history size * size of punctual observation (which is 2D,1D or scalar)]).
        a : list of ints with length (plan_depth+1)
            the action(s) considered at s1
        mask : 
        
        noise Es: shape of abstract repr
        
        noise tr : shape of abstract repr

        
        terminal : boolean
            Whether the transition leading to s2 is terminal
        
        Parameters
        -----------
        encoder_model: instantiation of a Keras model for the encoder (E)
        transition_model: instantiation of a Keras model for the transition (T)
        discrim_mask: instantiation of a Keras model for the discriminator (D)
        plan_depth: if>1, it provides the possibility to consider a sequence of transitions between s1 and s2 
        (input a is then a list of actions)
    
        Returns
        -------
        model with output Tx (= model estimate of x')
    
        """
        input_state=[]
        for i, dim in enumerate(self._input_dimensions):
            if(len(dim) == 4):
                input = Input(shape=(dim[-4],dim[-3],dim[-2],dim[-1]))
                input_state.append(input)
                input = Reshape((dim[-4]*dim[-3],dim[-2],dim[-1]), input_shape=(dim[-4],dim[-3],dim[-2],dim[-1]))(input)
            elif(len(dim) == 3):
                input = Input(shape=(dim[-3],dim[-2],dim[-1]))
                input_state.append(input)
            elif len(dim) == 2:
                input = Input(shape=(dim[-3],dim[-2]))
                input_state.append(input)
            else:
                input = Input(shape=(dim[-3],))
                input_state.append(input)
        
        enc_x = encoder_frozen_model(input_state)
        enc_x2 = encoder_model(input_state)
        
        # Apply a mask on enc_x2 used as input to the transition module
        if(self._high_int_dim==True):
            mask=Input(shape=(self.n_channels_internal_dim,))
            layers_mask=RepeatVector(self.n_rows*self.n_cols)(mask)
            layers_mask=Reshape((self.n_rows,self.n_cols,self.n_channels_internal_dim))(layers_mask)

            mask2=Input(shape=(self.n_channels_internal_dim,))
            layers_mask2=RepeatVector(self.n_rows*self.n_cols)(mask2)
            layers_mask2=Reshape((self.n_rows,self.n_cols,self.n_channels_internal_dim))(layers_mask2)
        else:
            mask=Input(shape=(self.internal_dim,))
            layers_mask=mask

            mask2=Input(shape=(self.internal_dim,))
            layers_mask2=mask2
            
        enc_x2=Multiply()([enc_x2,layers_mask]) # set to -1 if masked?          
        
        action=Input(shape=(self._n_actions,))
        
        if(self._high_int_dim==True):
            noise_Es = Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim) )
            noise_tr = Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim) )
        else:
            noise_Es = Input( shape=(self.internal_dim,) )
            noise_tr = Input( shape=(self.internal_dim,) )
        
        Tx = enc_x2
        Tx = Add()([Tx,noise_Es]) #Adding noise such that the learning is robust to noise in the abstract repr Es
        enc_x = Add()([enc_x,noise_Es]) #Adding noise such that the learning is robust to noise in the abstract repr Es
        
        x_, r, gamma = transition_model([Tx,action,noise_tr])
        
        if(self._high_int_dim==True):
            noise_Es2 = Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim) )
        else:
            noise_Es2 = Input( shape=(self.internal_dim,) )
        x_ = Add()([x_,noise_Es2]) #Adding noise such that the learning is robust to noise in the abstract repr Es

        # Apply a mask on x_
        x_=Multiply()([x_,layers_mask2]) # set to -1 if masked?          
        
        discrim = discrim_masked_model([enc_x,action,x_,mask,r, gamma])
        
        

#        #Rx=GaussianNoise(0.8)(Rx)
#        #gammax=GaussianNoise(0.8)(gammax)
#        #Tx=GaussianNoise(0.8)(Tx)
#        
#        #Tx = Conv2D(8, (3, 3), padding='same', activation='tanh')(Tx)
#        #Tx = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(Tx)
#        #Tx = Conv2D(8, (3, 3), padding='same', activation='tanh')(Tx)
#        #Tx = Conv2D(self.n_channels_internal_dim//2, (3, 3), padding='same', activation='tanh')(Tx)
#
#        # Also apply the mask to T(x) ? NO and YES!! -> in a smart way! FIXME
#        mask2=Input(shape=(self.n_channels_internal_dim,))
#        inputs.append(mask2)
#        layers_mask=RepeatVector(self.n_rows*self.n_cols)(mask2)
#        layers_mask=Reshape((self.n_rows,self.n_cols,self.n_channels_internal_dim))(layers_mask)        
#        Tx_masked = Multiply()([Tx,layers_mask])
#
#        input = Input(shape=(1,)) # 1-terminals (0 if transition is terminal)
#        inputs.append(input)
#        Tx_masked = Multiply()([Tx_masked,inputs[-1]])# set to 0 if terminal because we don't care about fitting that transition
#
#        discrim = discrim_masked_model(inputs[:len(self._input_dimensions)]+actions+[Tx_masked]+[Rx]+[gammax])
        
        model = Model(inputs=input_state+[action,mask,mask2,noise_Es,noise_tr,noise_Es2], outputs=discrim )
        
        return model


    def transition_model(self):
        """  Instantiate a Keras model for the transition between two encoded pseudo-states.
    
        The model takes as inputs:
        x : internal state
        a : int
            the action considered
        n : noise
            same size as internal state
        
        Parameters
        -----------
    
        Returns
        -------
        model that outputs 
        - the next abstract state x'
        - the reward r
        - the per time-step discount \gamma
    
        """
        if(self._high_int_dim==True):
            inputs = [ Input(shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim)), Input( shape=(self._n_actions,) ), Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim)) ]     # data_format='channels_last'
            
            layers_action=inputs[1]
            layers_action=RepeatVector(self.n_rows*self.n_cols)(layers_action)
            layers_action=Reshape((self.n_rows,self.n_cols,self._n_actions))(layers_action) #data_format='channels_last'
            
#            x = Concatenate(axis=-1)([inputs[0],layers_action,inputs[2]])            
#            x = Conv2D(16, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x)
#            #x = BatchNormalization(momentum=0)(x)
#            x = Conv2D(32, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x) #64
#            #x = BatchNormalization(momentum=0)(x)
#            x = Conv2D(64, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x) #128
#            x = Conv2D(128, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x) #256
#            #x = BatchNormalization(momentum=0)(x)
#            x = Conv2D(64, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x) #128
#            #x = BatchNormalization(momentum=0)(x)
#            x1 = Conv2D(32, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x)
#            #x1 = BatchNormalization(momentum=0)(x1)
#            
#            x_ = Conv2D(16, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x1)
#            #x_ = BatchNormalization(momentum=0)(x_)
#            x_ = Conv2D(8, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x_)
#            #x_ = BatchNormalization(momentum=0)(x_)
#            x_ = Conv2D(self.n_channels_internal_dim, (1, 1), padding='same')(x_) #if < 0.01/0.001, can't learn the correct dynamics!
#            x_ = Add()([inputs[0],x_])
#            
#            x1 = Conv2D(16, (3, 3), padding='same', activation='tanh')(x1)
#            #x1 = BatchNormalization(momentum=0)(x1)
#            x1 = Conv2D(8, (3, 3), padding='same', activation='tanh')(x1)
#            #x1 = BatchNormalization(momentum=0)(x1)
#            x = Flatten()(x1)
#            x = Dense(128, activation='tanh')(x)
#            #x = BatchNormalization(momentum=0)(x)
#            x = Dense(64, activation='tanh')(x)
#            #x = BatchNormalization(momentum=0)(x)
#            x = Dense(32, activation='tanh')(x)
#            #x = BatchNormalization(momentum=0)(x)
#            x = Dense(16, activation='tanh')(x)
#            #x = BatchNormalization(momentum=0)(x)
#            x2 = Dense(8, activation='tanh')(x)
#            #x2 = BatchNormalization(momentum=0)(x2)

            x = Concatenate(axis=-1)([inputs[0],layers_action,inputs[2]])            
            x = Conv2D(16, (1, 1), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Conv2D(64, (1, 1), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(x) #64
            #x = BatchNormalization(momentum=0)(x)
            xb = Conv2D(512, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(x) #128
            x = Conv2D(512, (1, 1), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(xb) #256
            #x = BatchNormalization(momentum=0)(x)
            x = Conv2D(512, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(x) #128
            x = Conv2D(512, (1, 1), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(x) #256
            #x = BatchNormalization(momentum=0)(x)
            x1 = Conv2D(512, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(x) #128
            #x1 = Add()([x1,xb]) #ResNet like
            #x = BatchNormalization(momentum=0)(x)
            x = Conv2D(64, (1, 1), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(x1)
            #x1 = BatchNormalization(momentum=0)(x1)
            
            #x_ = Conv2D(16, (3, 3), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(x1)
            #x_ = BatchNormalization(momentum=0)(x_)
            x_ = Conv2D(16, (1, 1), padding='same', activation='tanh', activity_regularizer=regularizers.l2(0.00001))(x)
            #x_ = BatchNormalization(momentum=0)(x_)
            x_ = Conv2D(self.n_channels_internal_dim, (1, 1), padding='same', activity_regularizer=regularizers.l2(0.00001))(x_) #if < 0.01/0.001, can't learn the correct dynamics!
            x_ = Add()([inputs[0],x_])
            
            x1 = Conv2D(64, (3, 3), padding='same', activation='tanh')(x1)
            x1 = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(x1) #important !
            #x1 = BatchNormalization(momentum=0)(x1)
            x = Conv2D(64, (3, 3), padding='same', activation='tanh')(x1)            
            x = Conv2D(64, (3, 3), padding='same', activation='tanh')(x)            
            x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(x) #important !
            #x = BatchNormalization(momentum=0)(x)
            x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
            #x1 = BatchNormalization(momentum=0)(x1)
            x = Flatten()(x1)
            x = Dense(256, activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Dense(64, activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            #x = Dense(32, activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            #x = Dense(16, activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            x2 = Dense(16, activation='tanh')(x)
            #x2 = BatchNormalization(momentum=0)(x2)
            
#            x = Concatenate(axis=-1)([inputs[0],layers_action,inputs[2]])
#            x = Flatten()(x)
#            x = Dense(256, activation='tanh')(x)
#            x = Dense(512, activation='tanh')(x)
#            x1 = Dense(512, activation='tanh')(x)
#            x_ = Dense(256, activation='tanh')(x1)
#            #print (self.n_rows*self.n_cols*self.n_channels_internal_dim)
#            #print (self.n_rows,self.n_cols,self.n_channels_internal_dim)
#            x_ = Dense(self.n_rows*self.n_cols*self.n_channels_internal_dim, activation='tanh')(x_)
#            x_ = Reshape((self.n_rows,self.n_cols,self.n_channels_internal_dim))(x_)
#            x_ = Add()([inputs[0],x_])
#
#            x = Dense(256, activation='tanh')(x1)
#            #x = BatchNormalization(momentum=0)(x)
#            x = Dense(64, activation='tanh')(x)
#            #x = BatchNormalization(momentum=0)(x)
#            x = Dense(16, activation='tanh')(x)
#            #x = BatchNormalization(momentum=0)(x)
#            x2 = Dense(8, activation='tanh')(x)
#            #x2 = BatchNormalization(momentum=0)(x2)
            


            r = Dense(4, activation='tanh')(x2)
            r = Dense(1)(r)

            g = Dense(4, activation='tanh')(x2)
            g = Dense(1)(g)

        else:
            inputs = [ Input( shape=(self.internal_dim,) ), Input( shape=(self._n_actions,) ), Input( shape=(self.internal_dim,) ) ]     # x

            x = Concatenate()(inputs)
            x = Dense(16, activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x) #activity_regularizer=regularizers.l2(0.001)
            x = Dense(64, activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x)
            x = Dense(256, activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Dense(512, activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x)
            x = Dense(1024, activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x) # NB: complex transition model
            x = Dense(512, activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x)  # along with complex discr model
            x = Dense(256, activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x)  # works well (at least as complex as discr)
            #x = BatchNormalization(momentum=0)(x)
            x1 = Dense(32, activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x)  # safe choice: use a quite complex one
            x_ = Dense(8, activation='tanh', activity_regularizer=regularizers.l2(0.0001))(x1)
            x_ = Dense(self.internal_dim, activity_regularizer=regularizers.l2(0.0001))(x_)
            x_ = Add()([inputs[0],x_])
                        
            r = Dense(8, activation='tanh')(x1)
            r = Dense(1)(r)

            g = Dense(8, activation='tanh')(x1)
            g = Dense(1)(g)
            
        
        model = Model(inputs=inputs, outputs=[x_,r,g])
        
        return model

    def transition_discr_model(self, discrim_mask=False):
        """  Instantiate a Keras model for the discriminator.
        Conditionally on (x,a), it discriminates whether the given (x_,r,g) comes from the distribution
    
        The model takes as inputs:
        x : internal state
        a : one-hot encoding of shape=(self._n_actions,)
            the action considered
        x_ : next internal state
        m : the mask
        r : int
            the reward
        g : int
            the per timestep discount
        
        Parameters
        -----------
    
        Returns
        -------
        model that outputs 
        - Boolean: whether the given transition is an actual transition (1) or generated (0)
    
        """
        if(self._high_int_dim==True):
            inputs = [  Input(shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim)), 
                        Input( shape=(self._n_actions,) ), 
                        Input(shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim)),
                        Input(shape=(self.n_channels_internal_dim,)), #mask
                        Input( shape=(1,) ), 
                        Input( shape=(1,) )  ]
            
            layers_action=inputs[1]
            layers_action=RepeatVector(self.n_rows*self.n_cols)(layers_action)
            layers_action=Reshape((self.n_rows,self.n_cols,self._n_actions))(layers_action)    #data_format='channels_last'
            
            layers_mask=RepeatVector(self.n_rows*self.n_cols)(inputs[3])
            layers_mask=Reshape((self.n_rows,self.n_cols,self.n_channels_internal_dim))(layers_mask)

            # Apply the mask on the input only for the regular discrim (not related to discrim_mask)
            if (discrim_mask==False): # usual discrim to fit T, r, g
                x_masked=Multiply()([inputs[0],layers_mask]) # set to -1 if masked?
                x__masked=Multiply()([inputs[2],layers_mask]) # set to -1 if masked?
            if (discrim_mask==True): # discrim for knowing whether there was a mask applied
                x_masked=inputs[0]
                x__masked=inputs[2] # mask already applied by full
            
            #layer_r=inputs[3]
            #layer_r=RepeatVector(self.n_rows*self.n_cols)(layer_r)
            #layer_r=Reshape((self.n_rows,self.n_cols,1))(layer_r)    #data_format='channels_last'
            #
            #layer_t=inputs[4]
            #layer_t=RepeatVector(self.n_rows*self.n_cols)(layer_t)
            #layer_t=Reshape((self.n_rows,self.n_cols,1))(layer_t)    #data_format='channels_last'

            x = Concatenate(axis=-1)([layers_action,x_masked,x__masked])#,layer_r, layer_t]) #does not work better
            
            x = Conv2D(16, (3, 3), padding='same', activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            #x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Conv2D(64, (3, 3), padding='same', activation='tanh')(x)
            x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(x) #important !
            #x = Conv2D(128, (3, 3), padding='same', activation='tanh')(x)
            #x = Conv2D(64, (3, 3), padding='same', activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Conv2D(64, (3, 3), padding='same', activation='tanh')(x)            
            x = Conv2D(64, (3, 3), padding='same', activation='tanh')(x)            
            x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(x) #important !
            #x = BatchNormalization(momentum=0)(x)
            x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            #x = Conv2D(self.n_channels_internal_dim, (1, 1), padding='same', activation='tanh')(x)
            x = Flatten()(x)
            #x = BatchNormalization(momentum=0)(x)
            add_inp = Concatenate()([inputs[4],inputs[5]])
            x = Concatenate()([x,add_inp])
            x = Dense(128, activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Concatenate()([x,add_inp])
            x = Dense(64, activation='tanh')(x)
            x = Dense(64, activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Concatenate()([x,add_inp])
            x = Dense(32, activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Concatenate()([x,add_inp])
            

        else:
            inputs = [  Input(shape=(self.internal_dim,)), #x
            Input( shape=(self._n_actions,) ), 
            Input( shape=(self.internal_dim,)), #x'
            Input( shape=(self.internal_dim,)), #mask
            Input( shape=(1,) ), 
            Input( shape=(1,) )  ]
            
            if (discrim_mask==False): # usual discrim to fit T, r, g
                x_masked=Multiply()([inputs[0],inputs[3]]) # set to -1 if masked?
                x__masked=Multiply()([inputs[2],inputs[3]]) # set to -1 if masked?
            else: # discrim for knowing whether there was a mask applied
                x_masked=inputs[0]
                x__masked=inputs[2] # mask already applied by full
                
            
            x = Concatenate()([x_masked,inputs[1],x__masked]+inputs[4:])
            x = Dense(64, activation='tanh')(x)
            x = Dense(256, activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Dense(512, activation='tanh')(x)
            x = Dense(512, activation='tanh')(x)
            x = Dense(256, activation='tanh')(x)
            #x = BatchNormalization(momentum=0)(x)
            x = Dense(64, activation='tanh')(x)
            
            
        x = Dense(32, activation='tanh')(x)
        #x = BatchNormalization(momentum=0)(x)
        #x = Dense(16, activation='tanh')(x)
        #x = BatchNormalization(momentum=0)(x)
        x = Dense(8, activation='tanh')(x)
        #x = BatchNormalization(momentum=0)(x)
        x = Dense(1, activation='sigmoid')(x)
        
        model = Model(inputs=inputs, outputs=[x])
        
        return model

    def transition_g_full_model(self, encoder_frozen, encoder, transition, transition_d):
        """  Instantiate a Keras model for the discriminator.
        Conditionally on (x,a), it discriminates whether the given (x_,r,g) comes from the distribution
    
        The model takes as inputs:
        noise Es: shape of abstract repr
        mask:
        s : list of objects
            Each object is a numpy array that relates to one of the observations
            with size [batch_size * history size * size of punctual observation (which is 2D,1D or scalar)]).
        a : one-hot encoding of shape=(self._n_actions,)
            the action considered
        
        Parameters
        -----------
        encoder: instantiation of a Keras model for the encoder
        transition: instantiation of a Keras model for the transition
        transition_d: instantiation of a Keras model for the discriminator of the transition
    
        Returns
        -------
        model that outputs 
        - Boolean: update the weights of the encoder and transition such that it looks like (x,a,r,gamma,x') (1)
    
        """
        dim=self._input_dimensions[0]

        if(self._high_int_dim==True):
            noise_Es = Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim) )
            mask = Input( shape=(self.n_channels_internal_dim,) )
        else:
            noise_Es = Input( shape=(self.internal_dim,) )
            mask = Input( shape=(self.internal_dim,) )
        
        input_state=[]
        if(len(dim) == 4):
            input = Input(shape=(dim[-4],dim[-3],dim[-2],dim[-1]))
            input_state.append(input)
            input = Reshape((dim[-4]*dim[-3],dim[-2],dim[-1]), input_shape=(dim[-4],dim[-3],dim[-2],dim[-1]))(input)
        elif(len(dim) == 3):
            input = Input(shape=(dim[-3],dim[-2],dim[-1]))
            input_state.append(input)
        elif len(dim) == 2:
            input = Input(shape=(dim[-3],dim[-2]))
            input_state.append(input)
        else:
            input = Input(shape=(dim[-3],))
            input_state.append(input)
        
        x = encoder_frozen(input_state)
        x = Add()([x,noise_Es]) #Adding noise such that the learning is robust to noise in the abstract repr Es
        
        x2 = encoder(input_state)
        x2 = Add()([x2,noise_Es]) #Adding noise such that the learning is robust to noise in the abstract repr Es
        
        action=Input( shape=(self._n_actions,) )

        if(self._high_int_dim==True):
            noise_tr = Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim) )
            layers_mask=RepeatVector(self.n_rows*self.n_cols)(mask)
            layers_mask=Reshape((self.n_rows,self.n_cols,self.n_channels_internal_dim))(layers_mask)
        else:
            noise_tr = Input( shape=(self.internal_dim,) )
            layers_mask = mask

        x2_masked=Multiply()([x2,layers_mask]) # set to -1 if masked?

        x_, r, gamma = transition( [x2_masked,action,noise_tr] )
                
        x_stop_grad = x #Lambda(lambda xx: K.stop_gradient(xx))(x)
        out_bool = transition_d([x_stop_grad,action,x_, mask, r, gamma])

        
        model = Model(inputs=[noise_Es]+input_state+[action,noise_tr,mask], outputs=[out_bool])
        
        return model

    def encoder_g_full_model(self, encoder_frozen, encoder, transition_d):
        """  Instantiate a Keras model for the encoder generator.
        Conditionally on (x,a), it discriminates whether the given (x_,r,g) comes from the distribution
    
        The model takes as inputs:
        noise Es: noise shape abstract repr
        s : list of objects
            Each object is a numpy array that relates to one of the observations
            with size [batch_size * history size * size of punctual observation (which is 2D,1D or scalar)]).
        a : one-hot encoding of shape=(self._n_actions,)
            the action considered
        s_
        r
        gamma
        mask:
        
        
        Parameters
        -----------
        encoder: instantiation of a Keras model for the encoder
        transition: instantiation of a Keras model for the transition
        transition_d: instantiation of a Keras model for the discriminator of the transition
    
        Returns
        -------
        model that outputs 
        - Boolean: update the weights of the encoder and transition such that it looks like (x,a,r,gamma,x') (1)
    
        """
        dim=self._input_dimensions[0]

        inputs=[]

        if(self._high_int_dim==True):
            noise_Es = Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim) )
        else:
            noise_Es = Input( shape=(self.internal_dim,) )

        input_state=[]
        if(len(dim) == 4):
            input = Input(shape=(dim[-4],dim[-3],dim[-2],dim[-1]))
            input_state.append(input)
            input = Reshape((dim[-4]*dim[-3],dim[-2],dim[-1]), input_shape=(dim[-4],dim[-3],dim[-2],dim[-1]))(input)
        elif(len(dim) == 3):
            input = Input(shape=(dim[-3],dim[-2],dim[-1]))
            input_state.append(input)
        elif len(dim) == 2:
            input = Input(shape=(dim[-3],dim[-2]))
            input_state.append(input)
        else:
            input = Input(shape=(dim[-3],))
            input_state.append(input)
        
        xxx = encoder_frozen(input_state)
        x_stop_grad = xxx#Lambda(lambda xx: K.stop_gradient(xx))(xxx) #xxx   # trainable = False instead of Lambda(lambda xx: K.stop_gradient(xx))(xxx)
                            # Otherwise bug 

        xxx = Add()([xxx,noise_Es]) #Adding noise such that the learning is robust to noise in the abstract repr Es

        action = Input( shape=(self._n_actions,) )

        input_state2=[]
        if(len(dim) == 4):
            input = Input(shape=(dim[-4],dim[-3],dim[-2],dim[-1]))
            input_state2.append(input)
            input = Reshape((dim[-4]*dim[-3],dim[-2],dim[-1]), input_shape=(dim[-4],dim[-3],dim[-2],dim[-1]))(input)
        elif(len(dim) == 3):
            input = Input(shape=(dim[-3],dim[-2],dim[-1]))
            input_state2.append(input)
        elif len(dim) == 2:
            input = Input(shape=(dim[-3],dim[-2]))
            input_state2.append(input)
        else:
            input = Input(shape=(dim[-3],))
            input_state2.append(input)

        x_ = encoder(input_state2)
        ###x_ = Add()([x_,noise_Es]) #Adding noise such that the learning is robust to noise in the abstract repr Es
        r = Input( shape=(1,) )
        gamma = Input( shape=(1,) )


        if(self._high_int_dim==True):
            noise_Es2 = Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim) ) #noise
            mask = Input( shape=(self.n_channels_internal_dim,) )
        else:
            noise_Es2 = Input( shape=(self.internal_dim,) ) #noise
            mask = Input( shape=(self.internal_dim,) )

        #inputs.append(Input( shape=(1,) )) #noise #FIXME
        #inputs.append(Input( shape=(1,) )) #noise #FIXME

        x_= Add()([x_,noise_Es2]) #Adding noise such that the learning is robust to noise in the abstract repr Es2
        #r = Add()([r,inputs[-2]])
        #gamma = Add()([gamma,inputs[-1]])
        #x_=Multiply()([x_,layers_mask]) # set to -1 if masked? #not needed --> will be done in transition_d

        
        out_bool = transition_d([x_stop_grad,action,x_, mask, r, gamma])
        
        model = Model(inputs=[noise_Es]+input_state+[action]+input_state2+[r,gamma,noise_Es2,mask], outputs=[out_bool])
        
        return model


    def Q_model(self):
        """ Instantiate a  a Keras model for the Q-network from x.

        The model takes the following inputs:
        x : internal state

        Parameters
        -----------
            
        Returns
        -------
        model that outputs the Q-values for each action
        """
        if(self._high_int_dim==True):
            inputs=[]
            outs_conv=[]
            for i, dim in enumerate(self._input_dimensions):
                # - observation[i] is a FRAME
                if len(dim) == 3 or len(dim) == 4:
                    input = Input(shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim)) #data_format is already 'channels_last'
                    inputs.append(input)
                    x = input     #data_format is already 'channels_last'
            
                    x = Conv2D(16, (2, 2), padding='same', activation='tanh')(x)
                    x = Conv2D(32, (3, 3), padding='same', activation='tanh')(x)
                    x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')(x)
                    x = Conv2D(16, (2, 2), padding='same', activation='tanh')(x)
                    x = Conv2D(4, (1, 1), padding='same', activation='tanh')(x)
                    out = (x)
                else:
                    print ("FIXME")
                        
                outs_conv.append(out)
            
            if len(outs_conv)>1:
                x = merge(outs_conv, mode='concat')
            else:
                x= outs_conv [0]
            
            # we stack a deep fully-connected network on top
            x = Flatten()(x)
            x = Dense(200, activation='tanh')(x)
        else:
            inputs = [ Input( shape=(self.internal_dim,) ) ] #x
            x = Dense(20, activation='tanh')(inputs[0])
        
        # we stack a deep fully-connected network on top
        x = Dense(50, activation='tanh')(x)
        x = Dense(20, activation='tanh')(x)
        
        out = Dense(self._n_actions)(x)
                
        model = Model(inputs=inputs, outputs=out)
        
        return model


    def full_Q_model(self, encoder_model, Q_model, plan_depth=0, transition_model=None, R_model=None, discount_model=None):
        """ Instantiate a  a Keras model for the Q-network from s.

        The model takes the following inputs:
        s : list of objects
            Each object is a numpy array that relates to one of the observations
            with size [batch_size * history size * size of punctual observation (which is 2D,1D or scalar)]).
        a : list of ints with length plan_depth; if plan_depth=0, there isn't any input for a.
            the action(s) considered at s
    
        Parameters
        -----------
        encoder_model: instantiation of a Keras model for the encoder (E)
        Q_model: instantiation of a Keras model for the Q-network from x.
        plan_depth: if>1, it provides the possibility to consider a sequence of transitions following s 
        (input a is then a list of actions)
        transition_model: instantiation of a Keras model for the transition (T)
        R_model: instantiation of a Keras model for the reward
        discount_model: instantiation of a Keras model for the discount
            
        Returns
        -------
        model with output the Q-values
        """
        inputs=[]
        
        for i, dim in enumerate(self._input_dimensions):
            if(len(dim) == 4):
                input = Input(shape=(dim[-4],dim[-3],dim[-2],dim[-1]))
                inputs.append(input)
                input = Reshape((dim[-4]*dim[-3],dim[-2],dim[-1]), input_shape=(dim[-4],dim[-3],dim[-2],dim[-1]))(input)
            elif(len(dim) == 3):
                input = Input(shape=(dim[-3],dim[-2],dim[-1]))
                inputs.append(input)
            elif len(dim) == 2:
                input = Input(shape=(dim[-3],dim[-2]))
                inputs.append(input)
            else:
                input = Input(shape=(dim[-3],))
                inputs.append(input)
        
        out = encoder_model(inputs)

        if(self._high_int_dim==True):
            inputs.append(  Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim) )  ) #noise
        else:
            inputs.append(  Input( shape=(self.internal_dim,) )  ) #noise
        
        out = Add()([out,inputs[-1]]) #Adding noise such that the Q-values learning is robust to noise in the abstract repr
        
        disc_plan = None
        disc_rewards=[]
        for d in range(plan_depth):
            inputs.append(Input(shape=(self._n_actions,)))
            inputs.append(Input( shape=(self.n_rows,self.n_cols,self.n_channels_internal_dim) )) #noise

            reward=R_model([out]+inputs[-1:])
            if(disc_plan == None):
                disc_rewards.append(reward)
            else:
                disc_rewards.append(Multiply()([disc_plan,reward]))
            discount=discount_model([out]+inputs[-1:])
            if(disc_plan == None):
                disc_plan=discount
            else:
                disc_plan=Multiply()([disc_plan,discount]) #disc_model([out]+inputs[-1:])

            out=transition_model([out,inputs[-2],inputs[-1]])
        
        if(plan_depth==0):
            Q_estim=Q_model(out)
        else:
            Q_estim = Multiply()([disc_plan,Q_model(out)])
            Q_estim = Add()([Q_estim]+disc_rewards)

        model = Model(inputs=inputs, outputs=Q_estim)
        
        return model

if __name__ == '__main__':
    pass
    