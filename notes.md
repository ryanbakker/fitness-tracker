# Python Machine Learning Fitness Tracker

###### Project based on a Masters Project by Dave Ebbelaar.

##### Tags

`MetaMotion Sensor` `Visualising Data` `Plotting Time Series Data` `Outlier Detection` `Chauvenet's Criterion`
`Local Outlier Factor` `Feature Engineering` `Frequency` `Low Pass Filter` `PCA` `Clustering` `Predictive Models`
`Naive Bayes` `SVMs` `Random Forest` `Neural Network` `Counting Repetitions` `Custom Algorithm`

### The Quantified Self

The quantified self is any individual engaged in the self-tracking of any kind of biological, physical, behavioural, or
environmental information. The self-tracking is driven by a certain goal of the individual, with a desire to act upon
the collected information –– Hoogendoorn, M., & Funk, B. (2018). Machine learning for the quantified self. On the art of
learning from sensory data.

### Raw Data Structure

The raw fitness data recorded by the MetaMotion sensor band, recording gyroscope and accelerometer is in CSV files. Both
of which are measure on the X, Y, and Z axis, with the accelerometer measured in geforce, and gyroscope in degrees per
second. Along with the axis vectors, they also have labels for data: epochs (ms), time (system time), and elapsed (
s) as the name of each file. The data was recorded by five separate individuals, including a light set and heavy set of
five different strength
training exercises. Each set for each individual has been recorded into a stand-alone csv file in raw data.

##### Note:

> The data also contains each individuals resting data while waiting to begin a set, sitting/walking between sets etc.

This means, specific files will need to be stitched together for the dataframe and given labels before we can feed them
to the input for the supervised learning model. The gyroscope data will be fairly larger than accelerometer as it runs
at a higher frequency, thus being able to record more data per second.