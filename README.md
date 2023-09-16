# Markov Chain Haiku Generator - Webapp
This is Haiku Generator project that leverages 1st-level and 2nd-level Markov Chaining (implented with hashmap) to create interesting poems.
Syllables are counted using the CMUDICT module in the Natural Language Toolkit (NLTK). The Markov Chain tables are trained on a corpus of 300+ haikus.
This project does absolutely nothing useful -- it is more an exercise in understanding Markov Chains and an excuse to learn Svelte.

It is deployed on Render, with the front-end being built on Svelte while the back-end is built on Flask. 
Sessions are used in order to regenerate lines of already generated haikus. Please enable cookies! 

The web-app works best on desktop browsers (tested on Chrome, Firefox)

Future updates include ChatGPT integration to "interpret" the deeper meaning behind the Markov-generated poems.

Link: https://frontend-vw1x.onrender.com/

![a](https://github.com/kevinluk1/HaikuGenerator/assets/71728686/5a20d0a3-b71d-49e4-be94-6cdc179ddcd4)


The idea for this project is based on Lee Vaughan's book, Impractical Python Projects. 


