import ollama
from utils.categorization_utils import extract_sections
from utils.config_utils import load_config

def generate_categorization(transcription):

    config = load_config()
    model_name = config['ollama']['model_name']


    prompt = f"""I have a transcript of a video, and I want to categorize its parts into four sections: Hook, Buildup, Body, and CTA.

    Please label each part accordingly without changing any content. The sections are defined as follows:

    - **Hook:** The opening statement that grabs the audience's attention. usually first few lines.
    - **Build Up:** The section that provides context or setup for the main content. It typically follows the hook and sets the stage for the detailed content. line following just after hook.
    - **Body:** The main content or detailed information. This is the bulk of the transcript where most of the information is shared. Rest part.
    - **CTA (Call to Action):** The closing statement that encourages the audience to take a specific action. Keep in mind that CTA is the last section of the transcript. Generally last few lines. You can pick the last 2-3 lines as CTA."


    Ensure the extracted sections are accurate and do not alter the content. Don't omit any single line in the Transcript. All the section are in order. 
    If any section is not found,  try to reiterate and look for it again. if still not found, then say: "The script provided does not contain a clear [section_name].

    Please extract and structure the provided text in the same way and place it below in the placeholders.
    Transcript:
        {transcription}

    Formatted Transcript:
        Hook: [Identify and label the hook here]

        Buildup: [Identify and label the buildup here]

        Body: [Identify and label the body here]

        CTA: [Identify and label the CTA here]
        
    """
    if model_name is None:
        model_name = 'phi3'
    
    print("Model Name:", model_name)
    response = ollama.generate(
        model=model_name,
        prompt=prompt,
        options={
            "seed": 42,
            "repeat_last_n": 33,
            "temperature": 0.7,
            "main_gpu": 0,
            "f16_kv": True,
            "use_mmap": True,
            "num_thread": 8
        }
    )

    hook, buildup, cta = extract_sections(response['response'])

    return hook, buildup, cta

if __name__ == "__main__":
    transcript = """ Multiple big creators stole my content and got millions of views, more views than even me, who is the original. Now, I could be mad at them, but I'm a giver and I will give you two of the best ways to find wild content they shouldn't steal, but use as inspiration. First is Tweet Hunter. Find a creator on Twitter in your space and go to their profile. Tweet Hunter will organize all the tweets by the most likes on the sidebar on the right. Scroll through and specifically look for Twitter threads. These are gold mines for video ideas. The second method is source TikTok. Find a creator on TikTok and use a Chrome extension to sort all their videos by the most views. Comment PB below if you want me to send you a link to these tools, plus a 22-page doc on how to grow your personal brand from scratch."""

    hook, buildup , body, cta = generate_categorization(transcript)
    
    print("Hook:", hook)
    print("Buildup:", buildup)
    print("Body:", body)
    print("CTA:", cta)