"""
Excute this experiment in 'experiments' directory
"""

from __future__ import absolute_import, division, print_function
import random, glob, math, os
import numpy as np
import pandas as pd
from collections import defaultdict
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
from PIL import Image
from screeninfo import get_monitors


def calc_VA(distance, size):
    return round(360 / math.pi * math.atan2(size, 2 * distance), 1)


def place_image(win, image_path, an2px, eccentricity, ori, size):
    stim = visual.ImageStim(
        win,
        image=Image.open(image_path),
        pos=(
            an2px * eccentricity * math.sin(math.radians(ori)),
            an2px * eccentricity * math.cos(math.radians(ori)),
        ),
        size=size,
    )
    return stim


try:  # try to get a previous parameters file
    exp_info = fromFile("lastParams.pickle")
except:  # if not there then use a default set
    exp_info = {"Observer": "unknown", "Session": "1", "Type[1: RDK; 2: Grating]": "1"}
exp_info["dateStr"] = data.getDateStr()  # add the current time

# present a dialogue to change params
dlg = gui.DlgFromDict(
    exp_info, title="Peripheral Vision Search Experiment", fixed=["dateStr"]
)
if dlg.OK:
    toFile("lastParams.pickle", exp_info)  # save params to file for next time
else:
    core.quit()  # the user hit cancel so exit

# Change working directory
if not os.path.isfile(os.path.basename(__file__)):
    os.chdir("./experiments")

# make a text file to save data
file_name = exp_info["Observer"] + "_" + exp_info["Session"] + "_" + exp_info["dateStr"]
# data_file = open(file_name+'.csv', 'w') # a simple text file with 'comma-separated- values'
# data_file.write('ori,sp,correct\n')

"""
From Yung-Hao San
notes: we used "hight" as units, my macbookpro is 18cm(900pixel), assume 57cm distance,
so 1 degree =50 pixel, 1/18 (.055) in ratio
below all use visual angle to caculate size, so always multiple an2ra

In My iMac,
Display Height: 33.5 cm (1890 pix)
Distance: 57.0 cm
i.e.
VA: 32.8 degree
1 degree: 1890 / 32.8 = 57.6 pix

In My Macbook Air 2017,
Display Height: 17.9 cm (900 pix)
Distance: 30.0 cm
i.e.
VA: 33.2 degree
1 degree: 900 / 33.2 = 27.1 pix
"""

# This version I used "pixel" as units
display_size = [get_monitors()[0].width, get_monitors()[0].height]
# VA = calc_VA(57.0, 33.5)
VA = calc_VA(57.0, 17.9)
an2ra = 1 / VA
an2px = round(display_size[1] / VA, 1)
print("Visual Angle: {}, 1 degree: {} pix, ".format(VA, an2px))

# presenting Concentric circles and lines for control panel
ConC = np.array([-0.3, -0.1]) * display_size[1]
ConS = np.array([6, 5, 4, 3, 2, 1]) * 1.4 * an2px  # 8.4, 7,5.6,4.2,2.8,1.4 VA


# 13 Classes
target_class = "cat"
non_target_classes = [
    "dog",
    "elephant",
    "tiger",
    "rabbit",
    "kangaroo",
    "sheep",
    "monkey",
    "lion",
    "bear",
    "fox",
    "pig",
    "otter",
]


# making condition list: 2 * 2 * 2 * 3 * 4 = 96 conditions
practice_list = []
condition_list = []
for size in [1, 2]:  # 2 stimuli size
    for rate in [1, 2]:  # 2 magnification rates to periphery
        for state in [0, 1]:  # 2 state (whether the target exists or not)
            practice_list.append(
                {
                    "size": size,
                    "rate": rate,
                    "state": state,
                }
            )
            for pos in [0, 1, 2]:  # 3 positions (0: center)
                for ori in [0, 1, 2, 3]:  # 4 directions
                    condition_list.append(
                        {
                            "size": size,
                            "rate": rate,
                            "state": state,
                            "pos": pos,
                            "ori": ori,
                        }
                    )

# Organize them with the trial handler for the practice section
practice = data.TrialHandler(
    practice_list,
    1,
    method="random",
    extraInfo={
        "participant": exp_info["Observer"],
        "session": exp_info["Session"],
        "MotionType": exp_info["Type[1: RDK; 2: Grating]"],
    },
)

# Organize them with the trial handler: repeated 2 times
trials = data.TrialHandler(
    condition_list,
    2,
    method="random",
    extraInfo={
        "participant": exp_info["Observer"],
        "session": exp_info["Session"],
        "MotionType": exp_info["Type[1: RDK; 2: Grating]"],
    },
)

# Store images path in dictionary
image_path_dict = defaultdict(list)
image_path_dict[target_class] = glob.glob("../data/{}/*".format(target_class))
for c in non_target_classes:
    image_path_dict[c] = glob.glob("../data/{}/*".format(c))


# Create window and stimuli,
win = visual.Window(
    display_size,
    allowGUI=True,
    color=(0, 0, 0),
    monitor="testMonitor",
    winType="pyglet",
    units="pix",
)

# Calcurate eccentricities of stimuli
eccentricity_level_1 = round(np.sqrt(2), 1)
eccentricity_level_2 = round(np.roots([1, -2, -7]).max(), 1)
eccentricity_level_3 = round(
    np.roots([1, -np.sqrt(2) - 4, 4 * np.sqrt(2) - 27]).max(), 1
)

# Dummy images
stim_list = []
dummy_path = "../data/dummy.png"
default_size = [an2px, an2px]
for i in range(12):
    if i < 4:
        stim_list.append(
            place_image(
                win,
                dummy_path,
                an2px,
                eccentricity_level_1,
                i % 4 * 90 + 45,
                default_size,
            )
        )
    elif 4 <= i < 8:
        stim_list.append(
            place_image(
                win,
                dummy_path,
                an2px,
                eccentricity_level_2,
                i % 4 * 90,
                default_size,
            )
        )
    else:
        stim_list.append(
            place_image(
                win,
                dummy_path,
                an2px,
                eccentricity_level_3,
                i % 4 * 90 + 45,
                default_size,
            )
        )
# for stim in stim_list:
#     stim.draw()

# Introduction messages
introduction_1 = visual.TextStim(
    win,
    pos=[0, 0.15 * display_size[1]],
    text="Please answer the question \nwhether cats exist in the stimuli.",
)
introduction_2 = visual.TextStim(
    win,
    pos=[0, 0.10 * display_size[1]],
    text="First, let's practice with some stimuli.",
)
introduction_3 = visual.TextStim(
    win,
    pos=[0, 0.05 * display_size[1]],
    text="Hit a Key when ready.",
)
# Fixation cross
fixation = fixation = visual.ShapeStim(
    win,
    vertices=((0, -an2px), (0, an2px), (0, 0), (-an2px, 0), (an2px, 0)),
    lineWidth=an2px // 2,
    closeShape=False,
    lineColor="white",
)
# Question
question_1 = visual.TextStim(
    win,
    pos=[0, 0.15 * display_size[1]],
    text="Was there cats?  Please press '0' or '1'.",
)
question_2 = visual.TextStim(
    win,
    pos=[0, 0.10 * display_size[1]],
    text="'0': No",
)
question_3 = visual.TextStim(
    win,
    pos=[0, 0.05 * display_size[1]],
    text="'1': Yes",
)
# Feedback
feedback_1 = visual.TextStim(
    win,
    pos=[0, 0.15 * display_size[1]],
    text="Your answer is correct!",
)
feedback_2 = visual.TextStim(
    win,
    pos=[0, 0.15 * display_size[1]],
    text="Your answer is incorrect.",
)
# Break
break_1 = visual.TextStim(
    win,
    pos=[0, 0.15 * display_size[1]],
    text="Please take a short break.",
)
break_2 = visual.TextStim(
    win,
    pos=[0, 0.10 * display_size[1]],
    text="If the experiment is ready, \nthe window will change to the fixation cross.",
)


# Show introduction messages
introduction_1.draw()
introduction_2.draw()
introduction_3.draw()
win.flip()
# pause until there's a keypress
event.waitKeys()


count = 0
globalClock = core.Clock()

result = pd.DataFrame(
    index=[],
    columns=list(condition_list[0].keys()) + [target_class] + non_target_classes,
)
# Start trials
for cur_trial in trials:
    # Store Data
    cur_stim = cur_trial

    # define motion direction ans speed
    trialClock = core.Clock()

    # Show fixation cross
    fixation.draw()
    win.flip()
    event.waitKeys()
    # Gitter
    core.wait(0.1)

    # Change non-target stimuli
    _non_target_classes = random.sample(non_target_classes, len(non_target_classes))
    for i, stim in enumerate(stim_list):
        image_path = random.choice(image_path_dict[_non_target_classes[i]])
        stim.image = Image.open(image_path)
        cur_stim[_non_target_classes[i]] = image_path

    # Change stimuli size
    for i, stim in enumerate(stim_list):
        stim.size = list(map(lambda x: cur_trial["size"] * x, default_size))
        if 4 <= i < 8:
            stim.size = list(map(lambda x: cur_trial["rate"] * x, stim.size))
        elif i >= 8:
            stim.size = list(
                map(lambda x: cur_trial["rate"] * cur_trial["rate"] * x, stim.size)
            )

    # Change target stimulus
    if cur_trial["state"] == 1:
        image_path = random.choice(image_path_dict[target_class])
        stim_list[4 * cur_trial["pos"] + cur_trial["ori"]].image = Image.open(
            image_path
        )
        cur_stim[target_class] = image_path

    # Draw stimuli
    for stim in stim_list:
        stim.draw()
    win.flip()
    core.wait(0.2)

    # Show the question
    question_1.draw()
    question_2.draw()
    question_3.draw()
    win.flip()

    flag = True
    while flag == 1:
        allKeys = event.waitKeys()
        for key in allKeys:
            if key in ["0", "1"]:
                cur_stim["ans"] = key
                flag = False
            elif key in ["q", "escape"]:
                print(result)
                result.to_csv("../data/result.csv")
                core.quit()

    result = result.append(cur_stim, ignore_index=True)

    if int(cur_stim["ans"]) == cur_trial["state"]:
        feedback_1.draw()
    else:
        feedback_2.draw()
    win.flip()
    event.waitKeys(maxWait=1, keyList=["space", "enter"])

    count += 1
    if count % (len(condition_list)) == 0 and count != len(condition_list):
        # Take a short break
        break_1.draw()
        break_2.draw()
        win.flip()
        core.wait(60)


# give some on-screen feedback
endthank = visual.TextStim(win, pos=[0, 0.15], color=(1, 1, 1), text="Thank you!")
endthank.draw()
win.flip()
event.waitKeys()  # wait for participant to respond

print(result)
result.to_csv("../data/{}.csv".format(file_name))

# trials.saveAsPickle(file_name='testData')

# Wide format is useful for analysis with R or SPSS.
# df = trials.saveAsWideText("testDataWide.txt")

win.close()
core.quit()
