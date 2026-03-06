# Tools installed

Doc used to remind me what I have installed, just in case I need to do it again.

I'd have a better list, but it seems the OSX terminal history was pruned.

- Anaconda
- MacPorts
- XQuartz
- JetBrains Complete - Free for educational use!

## MacPorts installed packages

```
sudo port install emacs
sudo port install emacs +x11
sudo port install texlive-latex
sudo port install texlive-latex +doc
sudo port install R +acelerate +aqua +java +latex +quartz +x11
sudo port install R +acelerate +aqua +java +latex +quartz
sudo port install R +acelerate +aqua +java +latex +quartz
sudo port install R +acelerate +aqua +java +latex +quartz
sudo port install R-app
sudo port install texlive-basic
sudo port install texstudio
sudo port load dbus
sudo port install hunspell-en_AU_large hunspell-en_CA_large hunspell-en_GB_large hunspell-en_US_large
```


## Emacs changes

Need to remap Option key, otherwise copy is hard to get to.

- Change Quartz to map Option to Alt.
- Change Terminal to map Option to Alt.
- Put the following in .emacs/init.el to map the keys to Meta.

```
;;; Mac keyboard - native version
(setq mac-option-modifier 'meta)
(setq mac-right-option-modifier nil)

;;; Mac keyboard - x11
(setq x-alt-keysym 'meta)

```
