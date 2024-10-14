import re

def extract_sections(response):
    hook_pattern = r"Hook:\s*(.*?)\s*Buildup:"
    buildup_pattern = r"Buildup:\s*(.*?)\s*Body:"
    cta_pattern = r"CTA:\s*(.*?)\s*$"

    hook_match = re.search(hook_pattern, response, re.DOTALL)
    buildup_match = re.search(buildup_pattern, response, re.DOTALL)
    cta_match = re.search(cta_pattern, response, re.DOTALL)

    hook = hook_match.group(1).strip() if hook_match else None
    buildup = buildup_match.group(1).strip() if buildup_match else None
    cta = cta_match.group(1).strip() if cta_match else None

    return hook, buildup, cta

if __name__ == "__main__":
    response = """Hook: Multiple big creators stole my content and got millions of views, more views than even me, who is the original.
                Buildup: Now, I could be mad at them, but I'm a giver and I will give you two of the best ways to find wild content they shouldn't steal, but use as inspiration.
                Body: First is Tweet Hunter. Find a creator on Twitter in your space and go to their profile. Tweet Hunter will organize all the tweets by the most likes on the sidebar on the right. Scroll through and specifically look for Twitter threads. The second method is source TikTok. Find a creator on TikTok and use a Chrome extension to sort all their videos by the most views.
                CTA: Comment PB below if you want me to send you a link to these tools, plus a 22-page doc on how to grow your personal brand from scratch."""
    hook, buildup, cta = extract_sections(response)

    print("Hook:", hook)
    print("Buildup:", buildup)
    print("CTA:", cta)