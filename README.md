# Edgeware++
**If you don't know what EdgeWare is, please go to the original page or scroll down to the original patchnotes at the bottom! This is just a modified version that adds new features!**

My goal with this extension of Edgeware is to add or modify features that I felt were missing or incomplete in the original version. I want to try to be as minimally intrusive as possible, i'm not aiming to remove or neuter any previous features, just add more functionality to the base program.

I have prior programming experience, but have never touched python before this project- so it's mostly going to be trial and error. Half of this is a learning experience made easier by horny motivation.

The EdgeWare++ Pack Editor is now live [here](https://github.com/araten10/EdgewareEditor-PlusPlus).

## New Features In Edgeware++:

•*Toggle that switches from antialiasing to lanczos, if Edgeware wasn't displaying popups for you this will fix that! (probably)*

•*Toggle to enable/disable desktop icon generation*

•*Ability to cap audio/video popups if so desired, audio was previously limited to 1 and videos were uncapped*

•*Subliminals now have a % chance slider, and can also be capped*

•*Can now change startup graphic and icon per pack, defaults are used if not included*

•*Added feature to ask you to confirm before saving if there are any settings enabled that could be "potentially dangerous", for those of you like me who initially wondered if edgeware would fuck up their computer*

•*Hover tooltips everywhere to help new users get a grasp on things without having to weed through documentation*

•*Edgeware installation now actually readable and gives info on first steps*

•*Toggle that allows you to close a popup by clicking anywhere on it*

•*Import/Export buttons are now in full view at all times at the bottom of the window*

•*Brand shiny new "Pack Info" tab that gives stats and information on the currently loaded pack*

•*Simplified error console in the advanced tab, which could potentially help bugfix some things*

•*Packs now support an "info.json" file which gives people basic information about the pack in the config window*

•*Overhaul to hibernate mode which allows you to choose between multiple different types, and have your wallpaper go back to normal after you close all the popups*

## Planned Additions:

•*Dark Mode*

•*Giving mitosis a percentage activation slider*

•*Giving a use to prompt/caption "moods", initial inspiration was giving people the ability to make "one handed" prompt modes, for those who are too "preoccupied" to type multiple full sentences*

•*Rewriting all the old config presets ~~to work with the new version~~, and a few new ones as well!* (turns out the old configs work fine (at least for me), but they could do with a little updating for new settings)

•*Allowing users to write config preset descriptions in the config window*

•*Allowing pack creators to somehow make Edgeware "change over time", for example, getting more depraved or having the themes change the longer it runs. Would likely use the mood system.*

•*Adding more in depth info to the pack info tab, but to do so I would like to make it so there's a "reveal spoilers" button*

I'm also wanting to add features to the pack editor, will probably do that when this is in a state where I feel mostly done with what I wanted to accomplish.

**Suggestions**

Suggestions I got from people who used the software and I thought would be interesting enough to try. Lower priority than my own planned additions, but still something I hope to add (or attempt to) in the future!

•*New type of popup: full screen text, taken from caption file. Like subliminals but briefly flashing on full screen.*

•*Randomized settings button. Might implement when i'm mostly done adding new config vars, but also gave me the idea for pack creators to be able to make "recommended settings" that you can switch to in the pack info tab*

## EdgeWare++ Patch Notes
**If you see that there's a new update and are somebody (like me) who is lazy and doesn't like installing every single update if unnecessary, here is how I do versioning:**

•+1.0 to version number: multiple new features, or a single large feature

•+0.5-0.25 to version number: new feature, but a smaller one or something not as essential, or lots of bugfixes

•+0.2-0.1 to version number: very small update, usually just a bugfix, accessibility options, UI tweaks

**Version 6**

**THE FUTURE OF EDGEWARE++**

You normally see this header when something is being deprecated, sunset, or no longer being worked on. Luckily I want to say right out the gate, that this is not the case. I do want to approach this subject though, as the next few updates might be a bit different than those previous.

I am nearing the end of my planned features for EdgeWare++, most of which are things that I went "man, it should have this as an option" when I first used the original program. Pretty much everything left is getting exponentially larger to tackle, which is partially why i've procrastinated on adding them. There's a bigger issue in the back of my mind though, and that's the pack editor. The more features I add to EdgeWare++ that let people do fun stuff with packs, the more the pack creator needs to know how to manually add in, since the pack editor is still configured to the base version and has no new features. Additionally, the pack editor is feature-light in general.

Because of this, I am planning to have version 7 or 8 be the *last version of EdgeWare++ for a while*. This is only because I want to focus instead on the pack editor, and I think it will only take 1-2 more versions to add the major features to packs that I want to add. After that, I might come back to EdgeWare++, I might take a break, I might be satisfied enough and move on, i'm unsure (mostly depends on how hellish it is switching to a new project). The last major features I want to add before then is mood blocking and "mood corruption", both of which I will go into more detail as they come out.

Of course, I could always get distracted and work on other stuff here first. This is not set in stone as I know full well that I get easily satisfied adding lots of small, easy features instead of huge ones that can take weeks to work on. Just wanted to lay out the groundwork and let people know what i'm thinking about moving forward.

•*Added troubleshooting option to disable connections to github for users with slow internet*

•*Added errors section to troubleshooting with some non-fatal errors able to print user-facing logs there (there are still more detailed logs in the subfolder, though!)*

•*Fixed some error checking \*ahem\* not existing, config should no longer crash if (most) non-essential files have errors in them*

•*Added official support for info.json in pack files.*
``{"name":"", "creator":"", "version":"", "description":""}``
>Anything left blank will be set to a default value. File does not have to be included at all, and all it does is give the user more information on your pack in the pack info tab. Max suggested characters for name/creator/version is 20, and any description longer than 400 characters will be cut off with [...]. I plan to put all of this in the pack editor soon with these values included.

•*Changed preset description to be handled by TextWrapper instead of the tkinter wraplength modifier*
>In short, things might look different than before but will wrap lines a lot cleaner

•*Added short hibernate mode timers to dangerous settings list*

•*Added feature in troubleshooting to skip directly to hibernate starting*

•*HIBERNATE OVERHAUL: added "hibernate types", which change how hibernate works. Also added a feature to change wallpaper back to your panic wallpaper once hibernate is done.*
>full documentation on the different hibernate types and how each one works is available in the "about" tab.

KNOWN ISSUES:

-Pump-Scare is not eligible for chaos, mostly because it taps into the popup itself directly and I want to get this update out sooner than later

-Hibernate modes might randomly drop popups, thus having less than expected range. This (shouldn't) affect the wallpaper fix setting, and upon testing an old version of edgeware this also happened with the original mode, so it might not be something worth fixing

**Version 5.2**

Small version while I mentally prepare for what i'm planning to do next...

•*Added feature to change icon file per pack. Uses "icon.ico" in the resources folder if there's one there, and default if not*

•*More tooltips!!!*

•*Added all of the currently added features to the top of the readme because honestly who wants to scroll down this far to get to the good stuff (is this even worth putting in the patch notes?)*

**Version 5.1**

It's the cleanup update!!!!!!! I recommend you do a fresh install, or at least delete the old clutter.

•*Moved max_subliminals and max_videos to /data/, because frankly I dont know what I was doing putting them in the root and I hated looking at them. The old ones can be safely deleted*

•*Deleted config-old, which was an ancient version of EdgeWare that didn't even run anymore*

•*Made the decision to turn on lanczos in the default config settings, because most people i've run into need to use it*

**Version 5**

Probably the **biggest** version yet if we're going by code added! But there's only two things changed:

•*Moved the import and export resources buttons to the bottom of the config window, and made them visible wherever you go*
>The people I have helped figure out EdgeWare with no prior experience had a near 100% confusion rate on what to do with packs, so I wanted to make it at least a little more clear. Might add a tooltip for them later.

•*Added a new tab: Pack Info, which allows you to see a ton of stats relating to the currently loaded pack. Current sections are Status, About, and Stats*
>This was a lot to add, so if there's any bugs with EW++ so far it'll all be here. Hopefully manages to be stable enough. Currently adding an about.json to your pack does nothing, but I wanted to add the framework for it since it's probably going to be one of my next added features.

**Version 4.8**

Wow, lots of small updates in a row!

•*Edited EdgewareSetup.bat to have easier to read text and also be more clear on next steps. It also now goes to config.pyw on completion rather than starting it immediately*
>Was helping somebody set up Edgeware and realized how confusing the initial startup is for some new users. Tried my best to demystify some of how to use it if you're not totally familiar with python programs. Changing it from start to config was so it didn't start barraging you with popups containing black circles before you even know what's going on

•*Further clarified a few things in the config window, added a tooltip or two, and added "troubleshooting" to the advanced tab name, since it contains a potentially important bugfix*

**Version 4.75**

•*Added troubleshooting tab and a setting to change from the antialiasing algorithm to lanczos*
>Some kind users on discord pointed out that popups weren't working, turns out somebody figured out that changing the resize algorithm from antialiasing to lanczos worked for them. This is code I didn't change for EdgeWare++, so maybe this has been a problem all the way from the original EdgeWare. Antialias has always worked for me, so to keep things as compatible as possible, i've added a toggle rather than just changing it over to the new algorithm. Hopefully this fixes some issues for people!

•*Added "buttonless" mode that allows you to click anywhere on the popup to close it*
>A feature request from discord, which somebody else already implemented for people who wanted it! Decided to add it as a toggle here. Thanks!

**Version 4.5**

•*Added version number, and EdgeWare Config checks to see if the GitHub is more up-to-date than your current version*
>I'm not planning on messing with any of the failsafes and auto-updates for the moment, and because of that I took out the not-implemented "download ZIP" button from the original release. This is so far the only thing i've removed from the original EdgeWare, but it also didn't do anything.

•*Added way more tooltips to things*

•*Fixed some dangerous option tooltip errors and added "Replace Images" as a dangerous option*
>I never used Replace Images and it turns out that it does what I thought "Fill Drive" did, so i'm glad I caught it while making tooltips!

•*Very minor changes on some button/slider labels for improved clarity*

**Version 4**

•*Finished max subliminals*

•*Added feature to receive warnings on having "dangerous" options enabled, will confirm with you before saving*
>The list of dangerous options are as follows: Run on Startup, Fill Drive, Timer Mode, Show on Discord, Disable Panic Hotkey, Run on Save & Quit. They are categorized into varying levels of severity.

•*Added tooltips on hover in the config window*
>Currently only added to the Warning on "Dangerous" Setting, mostly added to clarify which settings are considered "dangerous", but I might add it to more settings in the future so you don't have to cross reference the "about" page.

•*Added these patch notes in the "EdgeWare++" about page, because I forgot to do that last time*

**Version 3**

•*Added feature to change startup graphics per pack. File MUST be named "loading_splash.png" inside the resource directory. If none is found, automatically adjusts to the default.*
>After I set out to do most of what I want to accomplish i'm hoping to add these features to the pack editor so people actually know they exist

•*Actually made max video slider work properly. Max subliminals is still unfinished, but will be fixed next version (hopefully!)*
>Thank god! I spent double-digit hours trying to figure out how do to this the most gracefully (or at least efficiently) without rewriting the entire subprocess code, but in the end I opted for the easy/hacky way out. You'll see two new files appear in your edgeware directory, max_videos.dat, and max_subliminals.dat. These are files that only contain a single number, which is accessed and edited by the various popups to properly change the active number of popups. It's 4 AM right now and I want to push this before I forget, so right now only the video cap is fixed, but subliminals should be an easy addition now and will be done when I next work on EW++.

**Version 2**

•*Added feature to cap audio, and removed the hard-coded limit of 1 so multiple audio can play at the same time. The number goes down when audio finishes*
>I assume the intention of audio popups were things like long hypno files, which makes sense to limit to one. I wanted to expand this functionality to allow people to make packs that can layer shorter files, like layering multiple sex sounds on top of eachother. The default is still set to CAP ON with MAX 1 so if you are using old packs and don't want to touch this setting you don't have to do anything.

•*Added feature to cap videos in the config window, but is currently half implemented, so beware!*
>For specifics, the video capping feature works in the sense that it will cap the number of videos after a specific amount, but does NOT factor in video windows closing to lower the current videos playing count. I've been bashing my head against this problem for a while as it's much more complicated than other issues i've tackled in this project so far, but ended up wanting to take a break and finish/release some other elements of the program. I figured that since it technically "sort of" works and doesn't cause any instability or crashes (as far as i'm aware), I might as well include it in the release instead of commenting it out.

>If you want technical details, start.pyw calls popup.pyw as a subprocess, and passing variables to and from files like that is tricky (at least to me, with minimal python experience at time of writing). I've currently got start.pyw running a limiter "video number" variable that increases as it spawns new windows, but have struggled to find a way to get popup.pyw to reliably report back that a **video window** has closed and to get start.pyw to update the number whenever that happens. I will continue to try and figure out ways to do this without causing major performance/stability issues.

•*Moved the Subliminals option down to it's own section*

•*Added feature to give subliminals a percentage chance to activate. Defaults at 100, which is the same as the original EdgeWare*

•*Added option in the config menu to limit max number of subliminals, but it currently does nothing*
>Pretty much the exact same issue as the max video problem above, although this one might be easier to solve. However, unlike the max video slider, this truly does absolutely nothing and won't impact anything in the current version. I'm probably unprofessional for not disabling or removing this in the current version.

**Version 1.1**

•*Added change notes in about section*

**Version 1**

•*Added a option under "misc" to enable/disable desktop icon generation*

•*Old presets from the original edgeware still exist, but may have compatibility issues.*

Original Edgeware patchnotes included below for posterity.

# Edgeware
**First and foremost as a disclaimer: this is NOT actually malicious software. It is intended for entertainment purposes only. Any and all damage caused to your files or computer is _YOUR_ responsibility. If you're worried about losing things, BACK THEM UP.**

If you get error "TypeError: unsupported operand type(s) for |: 'type' and 'type'", please make sure your Python is up to date! This version was primarily developed on Python 3.10.2!

2.4.2_A Update

•*Fixed bugs with popups that caused videos and subliminal adjusted images to not load properly*

(Small) 2.4.2 Update

•*Popups should open faster and take up less memory while running*

•*Added a small message in the Booru Downloader section of config*

Hiya! I'm not dead! This update fixes some issues with popups that have been nagging at me in the back of my head for a while and adds a direct, in-application answer to the most common question I get messages about. I'd like to come back to the project when I have some more time, and it's possible that a code overhaul is in the future, but as life tends to be a roller coaster I can make no definite promises for the timeframe of that sort of an update. But know that this is a project I hope to fix up in the future, even if there will be fewer new features added with time.

Bugfix Version 2.4.1_2 Update

•*Properly re-fixed the issue causing config to corrupt the config file under specific circumstances which resulted in start and config crashing*

Bugfix Version 2.4.1_1 Update

•*Fixed Run on Startup*

Version 2.4.1 Update

•*Fixed bug where start and config would crash on startup for new users due to PIL not being properly placed into the safe import blocks*

Version 2.4.0 Updates

   _**[Large Additions]**_

•**Timer Mode** *Timed runs can now be set, during which the Panic features cannot be used (unless a password is set and used). Run on startup is also forcibly enabled during this time.*

•**Mode Presets** *Config files can now be saved as "Presets," and can be freely swapped between in the config menu itself. These can have descriptions along with them, stored as [preset name].txt text files inside the preset folder.*

•**Lowkey Mode** *A more laid back way to enjoy Edgeware, but more active than Hibernate Mode. Popups will flash from corner to corner before slowly fading away and being replaced by another new popup.*

•**Denial Mode** *While Denial Mode is toggled, popups can randomly be blurred out or otherwise censored. Text will appear on top of them, either a default phrase or a phrase selected from the captions.json file under the "denial" tag.*

•**Popup Subliminals** *Popups can now have subliminal gifs overlayed on top of them. To accompany this, a "submliminals" folder is now supported in resource packs, from which a subliminal gif will be randomly selected and overlayed on top of the image. If none are present, the default gif in default_resources will be used.*

     •*Please be aware that this feature can potentially be very memory/cpu intensive and set your popup fadeout accordingly.*

•**Booru Downloader Update** *The previous booru downloader was incompatible with Rule34, and had actually completely broken due to a Booru update. The new version is more efficient and easier to maintain/fix if the issue arises again, and is also now able to handle exceptions to standard Booru URLs like Rule34.*

  _**[Small Additions]**_

•**Logging** *Start, config, and popup now all generate log files detailing their operation and any errors they encounter with greater detail.*

•**Panic Wallpaper** *Panic wallpaper is now previewed in the config menu, and can be changed to an image of your choice there, under the wallpaper tab.*

•**Debug Tool** *For other errors/viewing of print statements, a small debug batch tool has been added.*

•**Popup Opacity** *Added a new opacity setting for popups.*

•**Tray Icon** *Added a tray icon for Edgeware, which allows you to easily use the panic feature even while no popups are on the screen without manually running the panic files.*

   _**[Updated Features]**_

•**Panic Button** *The panic button is now "e" by default instead of "\`".*

•**Fill Delay** *Updated fill delay setting, now ranges from 0ms to 2500ms instead of the previous 0-25ms.*

•**Video Player** *Videos no longer play in a web browser, and instead now play in popup windows. The volume of the videos can also be configured on the config menu.*

•**Audio Handling** *Updated how audio is played, so now mp3 OR wav files, probably others too but I haven't tested them.*

•**Wallpaper Handling** *Updated wallpaper handling, which should result in wallpapers being more stable for config to handle, and prevent any accidental self doxxing when sharing config files.*

•**Library Imports** *Updated library importing at the start of start and config. Much more standardized and no longer requires checks in the config file.*

•**Config Layout** *Config layout has been updated, with features being more spaced out.*

•**General Standardization** *Start and Config have been updated to make their code more standardized. (I did my best to comply with pep8 but I'm very stupid so please bear with me programmers)*

•**Advanced Tab** *Minor adjustments to the Advanced tab layout, bringing it into line with the rest of the config menu.*

   _**[Bugfixes]**_

•**Popup Borders** *Popups now properly have borders that go all the way around the image instead of just the top and left sides.*

•**Config/Start Crash** *Fixed bug where the config file would be corrupted by config.cfg saving wallpapers in a certain configuration.*

•**Wallpaper Crash** *Fixed bug where missing wallpaper setting would cause config to crash when opening.*

•**Run on Startup Failure** *Fixed bug where the startup bat would not be placed into the windows startup folder. (This should be fixed, but it's always possible I just fixed a different but connected issue instead.)*

   _**[Additional Note]**_**

Hello! This will likely be the last update (or at least, last main release version) of Edgeware for the time being. Unfortunately with the constraints of life and my declining interest in porn, it's become more and more difficult to maintain the project as I had originally planned to. It does make me very happy that so many people enjoy my work, and I hope that this update can at least make it feel a bit more complete for you all. I'm very thankful for all the kind words I've received regarding the project, and maybe one day I'll be back to make more updates, but for now I'll be focusing on life and other projects. I'll also be sporadically available on my Twitter to answer tech support questions or just chat. I love you all and please take care of yourselves! <3

_**[How to Use]**_

Start by downloading this repository as a zip, and then extracting it somewhere on your computer.

(*If not using a premade package, skip this step.* )
Download one of the premade packages listed below. Once it's downloaded (if using a premade package), place it into the Edgeware folder inside Edgeware-main.

Double click "EdgewareSetup.bat" and follow the instructions. It should check your Python version, and then automatically download the correct installer from python.org and run it. Once you finish with that installation, it will run start.pyw, which will walk through an automated first time setup. Once this setup is complete, it will provide you with the config window to select your settings, and then run! (The installations only need to be performed on the first run)

   _**[Premade Packages]**_

**Blacked**

*Standard Blacked hentai stuff, includes Porn Addict Brainwash Program: BBC Edition, and some volafile mp3s from /trash/ Blacked threads*

https://drive.google.com/file/d/1BHLrCO5cvm9YCF_EeWGYS8AmAsPxUZPJ/view?usp=sharing

https://mega.nz/file/IfJS1JLB#eEkreHNBH5g_maKsiUC0I1BOeh1FvdOwU5i-Eto6FwA

**Gay Yiff**

*Includes lots and lots of steamy, hulking furry cocks*

https://drive.google.com/file/d/1b2gOJBLy-nD5p1cOM8xTDPh7LGsf1g58/view?usp=sharing

https://mega.nz/file/kOA2DZAJ#5A7pfQUdEKq8s3ner4dhmrKxS7xoYupMcNAAK3voU3M

**Censored**

*For the people who get off to not getting off*

https://drive.google.com/file/d/1phBN4JhoyOg3yAMomGgIKVTryYc8dv4Q/view?usp=sharing

https://mega.nz/file/lPBUxRyA#AJlC4Kwrtdci3cjISWkZ8YThuWEmyHcL81MfZoprrqQ

**Hypno**

*Includes the most gifs of any pack by far, as well as Porn Addict Brainwash Program 5 & 6, and Queue Balls 1*

https://drive.google.com/file/d/1W2u_wAp2DAWa-h0O5VUlGKhKSVMwQkh5/view?usp=sharing

https://mega.nz/file/YHB2ABAa#QApGJHeg6EF-20VP0OVf8yZyQtmCdZRQduXrHOHvUCM

**Hentai/Basic Gooner**

*Includes mostly 3D or hentai images, has 100% gifs, some videos, and audio from the porn addict brainwash program and queue balls*

https://drive.google.com/file/d/10_t11qm_2fRp4GVh0JK4hskdwW9ppCme/view?usp=sharing

https://mega.nz/file/gWwDmYJT#xWGsdfaPB5TvsnvDC4OUEWR06flqn7Bc9pvOErSUBuY

**No Limit Gooner**

*Includes the same audio as Hypno, as well as an MLP worship themed hypnosis file by https://twitter.com/AlmondMilkomg. Heavier focus on stranger kinks such as ponies, furry, farts, cringe, emoji, etc.*

https://drive.google.com/file/d/1nExnM00ODbZjAV2w8UX-Ybw8wp3ffNjK/view?usp=sharing

https://mega.nz/file/0SQEzZrb#UK6SSDUFz8u_xM5lcNMStqQdS-bqE_ilB6u7RkGUjGM

**Elsa**

*More or less all of the original assets and resources from the original Elsavirus. It's not a 1:1 experience, but if you liked the Elsa theming and original writing, it's all still there.*

*Warning that this pack does contain ALL of the resources from the original Elsavirus, including the noose image.*

https://drive.google.com/file/d/1QLJI52zM9HrJP_ozNxLaUSSEVUoDpjJP/view?usp=sharing

https://mega.nz/file/JKRCHR4a#SnxrAar_rvhK4BYjewz1TZmtV6EEeyEG9QU8JTkWOck

**Futanari**

*Futa themed pack, includes some generic moaning and plap plap audio. This and the Elsa pack are the first to make use of the caption feature, older packs will be updated with new resources and caption assets in the coming weeks.*

https://drive.google.com/file/d/12L9lKiOzKgBlDaoPudNhkYgZH-3khUeh/view?usp=sharing

https://mega.nz/file/AWQUTDYb#1rjRbHbDfqTVt-w7m-IryWFAf95us0tg3kBq-5VybGw


__**FAQ**__

**Q: "Why do I keep getting white circles in my popups?"**

**A: *This occurs when the resource folder is generated without any resource zip in the script folder. Either delete your resource folder and restart Edgeware with the zip located properly or manually import your zip with the config function.***

**Q: "Where does the booru downloader save files?"**

**A: *The booru downloader saves all files it downloads into the /resource/img/ folder.***


__**What is Edgeware?**__

Edgeware is an Elsavirus inspired fetishware tool, built from the ground up to use interchangeable resource packages for easily customized user experience.

Much like Elsavirus and Doppelvirus, this program was written in brainlet level Python, but unlike the two of them, has no compiled executables. If you're the type to fear some hidden actually malicious scripts, this ensures that *all* of the code is front and center; no C++/C# forms or other tricks that might hide the true nature of the application.


The software features the popups, hard drive filling, porn library replacing, website opening features of its predecesors.

Edgeware *does* include some unique features to make it more widely applicable than just the previous respective target demographics of /beta/ participants and finsub followers. Namely its packaging system, which allows anyone to cater the experience to their own particular interests or fetishes. Either place a properly assembled zip file named "resources.zip" in the same folder as the scripts so that the program can unpack it or manually extract the resources folder into the said directory.

I more or less went into this wanting to make my own version of Elsavirus/Doppelvirus for fun, but figured around halfway that it might be worthwhile to share it with others who might have similar tastes.

Obviously you need to have Python installed, but other than that there should be no dependencies that aren't natively packaged with the language itself.

__**Packages**__

  Packages must be structured as follows:

    (name).zip
       ->aud
         (Audio Files) (Optional)
       ->img
         (Image Files, Gif Files)
	   ->subliminals
	     (Gif files only) (Optional)
       ->vid
         (Video Files) (Optional)
       icon.ico
       wallpaper.png
       web.json (Optional)
       prompt.json (Optional)
	   discord.dat (Optional)
	   captions.json (Optional)

  The web.json file should contain two sets:

    {"urls":["url1", "url2", ...], "args":["arg1,arg2,arg3", "", "arg1,arg2", ...]}
    ->urls - set of urls
    ->args - corresponding set of arguments; even if a url should take no argument, there must be a "" in this
      ->args are separated by commas within their strings, eg "arg1,arg2,arg3"
      ->ensure that urls and args are aligned; if the first URL can take the args "a,b" the first args value should be "a,b"
      ->args will be selected randomly and appended to the end of the url
        ->eg, "https://www.google.com/" with args "penis,cock,ass" cound randomly return one of
        ->https://www.google.com/penis  https://www.google.com/cock  https://www.google.com/ass

  The prompt.json file should contain any number of sets:

    {"moods":["mood1", "mood2", "angryMood"], "freqList":[10, 40, 50], "minLen":2, "maxLen"=4, "mood1":["mood1 sentence 1.", "mood1 sentence 2."], "mood2":["mood2 only has 1 sentence."], "angryMood":["angryMood also has one sentence."]}
        ->moods - names don't matter, as long as they're accounted for later in the set.
        ->freqList - correspond to each value in moods, define the frequency of that mood being selected.
        ->min/maxLen - minimum number of sentences that can be selected vs maximum.
        ->mood name
            ->can contain any number of mood related sentences.
            ->will ONLY select from this set if that mood is selected.

If resources are present, but not properly structured, the application could crash or exhibit strange behavior.

*(If you like my work and would like to help me pay for food, please feel free to donate; Cashapp is $PetitTournesol)*
