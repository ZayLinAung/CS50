Traffic Project Experimentation

To get the model for the compiled neural network, I first started with the same model used in the lecture for handwritten program. These include the following layers

- One convolutional layer with 32 filters
- One max-pooling layer 
- One layer for flatten units
- One hidden layers with 128 units using RELU activation
- 50% dropout rate layer
- One output layer with NUM_CATEGORIES units

**Trial 1**

On the first trial, I just started with the identical model from the lecture and the result is terrible with very low accuracy percent. 

Training accuracy - 5.5%
Testing accuracy - 5.65%

**Trial 2**

The first thing I did to modify the model is adding two more layers: one convolutional layer with 32 filters and one max-pooling layer to extract additional features. Doing this alone incredibly increases the accuracy rate as below. However, this still does not meet the satisfactory level. 

Training accuracy - 89.13 %
Testing accuracy - 94.51%

**Trial 3**

In trail 3, I decided to add two more hidden layers with 128 units each. Another great improvement in accuracy rate was found. 

Training accuracy - 93.18%
Testing accuracy - 93.05%

**Final Trial**

As for final trial, I became a bit curious and wanted to test if there was a better way to improve the accuracy. Thus, I increased the number of filters in each convolutonal layer to 64 filter and increase the number of units to 512 in one of the hidden layer. My final testing accuracy is listed as follow.

Training accuracy - 95.43%
Testing accuracy - 95.53%



