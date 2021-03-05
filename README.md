# Eye Tracking experiments with Tobii Pro Spectrum

## Environments
- Python 3.6
- Psychopy 3.0

## Features of the Experiments
- Switch the image whether you gaze the left side or right side of the screen
- Track your eyes


## Usage
### 1. Clone this reopsitory
```
$ git clone https://github.com/Tiger-0512/tobii-experiments.git
```

### 2. Create conda environment
```
$ cd tobii-experiments
$ curl https://raw.githubusercontent.com/psychopy/psychopy/master/conda/psychopy-env.yml > psychopy-env.yml
$ conda env create -n psychopy -f psychopy-env.yml
```
Check [this page](https://www.psychopy.org/download.html) for more information.

### 3. Run Psychopy
```
$ conda activate psychopy
$ psychopy
```

### 4. Save Eye Tracker Calibration Data
Use [Tobii Pro Eye Tracker Manager](https://www.tobiipro.com/product-listing/eye-tracker-manager/) to calibrate.<br>
Once you calibrate your eye, the parameter is saved in the eye tracker internally.<br>

### 5. Excute the experiments
In PsychoPy editor, select the experiment in this repo and the run it.

## Notice
Any sampling rate is OK when you calibrate your eye.