# Smart Reach

This is python scripy which automated the process of mailing recruiters/HRs by using gen-ai. Using gen-ai the cold mail is curated in the best way possible.

This is a python script follow the instructions given below to run the script

## Setup

1. Clone the repository:

```bash
git clone https://github.com/scienmanas/Smart-Reach
```

2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Set up the environmental variables

| ENV variabkes  | Description                    |
| -------------- | ------------------------------ |
| NAME           | Your Name                      |
| EMAIL          | Your email                     |
| PASSWORD       | Email App Password             |
| SMTP_HOST      | SMTP host name                 |
| PORT           | Email server port number (587) |
| GEMINI_API_KEY | Gemini api key                 |

## Running the Script


## Troubleshooting

1. In Linux systems you need to create a virtual environment and then install the requirements.txt if your updated your system recently.
2. APP password in different from your normal password of your email, please first enable the MFA(Multifactor authentication) to set it in your email account.
3. If you are using email provided by `gmail` then the `SMTP_HOST` is `smtp.gmail.com`.
4. If you face any other issues, please email me or raise an issue in the repository.

## Demo

<iframe width="560" height="315" src="https://www.youtube.com/embed/hxg3AhYs-7I?si=VnJrhb_I78Ai-VxO" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>