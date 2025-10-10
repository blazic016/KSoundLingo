```

WORD/PHRASE TEMPLATE 

The section between %%level,isword,enable%% defines additional information about the translation based on the JSON fields.

%%
1) Level: A1 or A2 or B1 or B2
2) W or P (Word or Phrase)
3) E or D (Enable or Disable)
%%

EXAMPLE OF ENABLED WORD
	%%A1,W,E%% Target Word - Native Word
	A1 - means level A1.
	W - means that it is a word (not a phrase).
	E - indicates that the item is enabled for markdown and audio generation.

EXAMPLE OF DISABLED WORD
	%%A1,W,E%% Target Word - Native Word
	A1 - means level A1.
	W - **means that it is a word (not a phrase).**
	E - means that is Disabled for generating markdown and audio sound.

EXAMPLE OF ENABLED PHRASE
	%%A1,P,E%% Target Phrase - Native Phrase
	A1 - means level A1.
	P - means that it is a prahse (not a word).
	D - indicates that the item is disabled for markdown and audio generation.
	
	
CATEGORY TEMPLATE
	### Target word/phrase - Native word/phrase
	Category always starts with '###' to indicate that it is a title.
	In the category, the following are not defined: level (A1, A2, B1, B2), word/phrase (W, P), enabled (E, D).
	It is always included as a translation during audio generation.

```
### **Köszönések és alap kifejezések - Pozdravi i osnovne fraze**
%%A1,W,E%% Szia - Zdravo  
%%A2,P,D%% Viszlát - Ćao (pri rastanku)  
%%A1,W,E%% Jó reggelt - Dobro jutro  
%%A2,W,E%% Jó napot - Dobar dan  
%%B1,P,D%% Jó estét - Dobro veče  
%%A1,P,E%% Jó éjszakát - Laku noć  
%%B2,P,E%% Hogy vagy? - Kako si?  
### **kérdés - pitanje** 
%%A1,W,E%% **ki** – ko
%%A1,W,D%% **kik** – ko (u množini, „ko sve“)
%%A1,W,E%% **mi** – šta
%%A1,W,D%% **mik** – šta (u množini, „koje stvari“)
%%A1,W,E%% **hol** – gde


