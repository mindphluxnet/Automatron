## Automatron
A ***very*** much work-in-progress project for ChatGPT automation, inspired by AutoGPT.
I enjoyed their idea but not the implementation and I'm always eager to learn stuff so I decided to attempt to roll my own.

### Installation

You need a ***paid*** ChatGPT API key before you can even attempt to use this. 

Also requires the Git command line utility to be installed on your system. Get it at https://www.git-scm.com/downloads
- Clone the repository.
- install requirements with ```pip install -r requirements.txt```
- Rename ```.env-dist``` to ```.env``` and edit it to include your ChatGPT API key. Also fill in any other API keys you might encounter (so far only for Google Custom Search Engine).
- Run with ```python main.py```

### Caution!

So far there's only a handful of commands implemented that ChatGPT can use and thus it doesn't get very far in terms of automation.
However, as commands are plugins it's easy to expand. It's really a work-in-progress and shouldn't be taken as anything but an extremely early alpha.

Be aware that experimenting with this can become rather expensive as the token usage for even the most basic queries is rather high due to the amount of instructions supplied to ChatGPT on each query.
