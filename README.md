# PaperMWPFEvaluation


To minimize the speed evaluation error on MacOS, check the pid of the worker jobs and then set the NICE values as follows:
```sh
htop  # 48348-48353

sudo renice -n -20 -p 48348
sudo renice -n -20 -p 48349
sudo renice -n -20 -p 48350
sudo renice -n -20 -p 48351
sudo renice -n -20 -p 48352
sudo renice -n -20 -p 48353
```
