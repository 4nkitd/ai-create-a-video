# Create Video Using Ai
This is a project that uses OpenAi's ChatGP to create a video using the news api.

<!-- Show Example Output -->
## Example Output
[Youtube Link - https://youtu.be/0InpG3Au8n0](https://youtu.be/0InpG3Au8n0)
<video src="./final_video_try_1.mp4"></video>


<!-- paragraph explains main.py  -->
## How Does this work
Step 1. Get what to make the video about from the news api.
Step 2. Create a Custom Prompt using the Response from api.
Step 3. User OpenAi to Generate Video script using the prompt.
Step 4. Split THe Response into sentences by splitting it at the full stop and "," comma.
Step 5. Create a video using the sentences as the text for each frame.

<!-- paragraph explains how to use the code --> 
## How to use
1. Clone the repo
2. Install the requirements
3. Run the main.py file

## Skills Used
- ChatGP | OpenAi
- Python
