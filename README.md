# saltyapi
## Description
The saltyapi is an api that takes translation requests and returns a translation using Google Translate or DeepL translation services.
## Background
In Resonite, any items created and shared can be reverse-engineered by other users. I wanted to give users the ability to translate messages using Google Translate as a part of my Mute Helper system, but in doing so I would have had to embed my Google Translate API key into the in-game object. This Key does not have enough options given to me by Google to make it safely sharable without users being able to take actions that would cost me a lot of money in usage fees. As a solution, I have developed this middleman server that translates requests for end-users, while also doing it in a limited way and respecting my monthly usage quotas. As an added bonus, this API also has the option to use the DeepL translation service. 
### Statistics
2024: over 2.6 million characters translated by Resonite users across Google and DeepL APIs
