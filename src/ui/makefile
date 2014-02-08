UIC ?= pyside-uic
RCC ?= pyside-rcc

UIFILES :=  explorer.ui findred.ui tagpanel.ui

RCFILES :=
SUBDIR := 

PYUIFILES := $(UIFILES:%.ui=%.py)
PYRCFILES := $(RCFILES:%.qrc=%_rc.py)

all : ui $(SUBDIR)
	
ui: $(PYUIFILES) $(PYRCFILES) $(SUBDIR)


$(PYRCFILES) : %_rc.py : %.qml
	$(RCC) $*.qrc -o $@
	
$(PYUIFILES) : %.py : %.ui
	$(UIC) $< -o $@

clean: $(SUBDIR)
	rm -rf $(PYRCFILES) $(PYUIFILES)

clean_rc: $(SUBDIR)
	rm -rf $(PYRCFILES)


.PHONY: $(SUBDIR)
$(SUBDIR):
	$(MAKE) -C $@ $(MAKECMDGOALS)
