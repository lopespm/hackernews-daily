# Hacker News Daily

![Hacker News Daily Intro Image](https://user-images.githubusercontent.com/3640622/103142583-4e581e00-46fd-11eb-9331-ce821830d4e0.png)

Website accessible at **[https://lopespm.github.io/hackernews-daily](https://lopespm.github.io/hackernews-daily)**

More details about this implementation **[in this blog article](https://lopespm.github.io/2020/12/25/hackernews-daily.html)**

Features:
- Best Hacker News stories from the past 10 days, or from the most recent day. Updated every day
- Web Page screenshot and top comments for each story
- Responsive layouts for Mobile and Desktop
- Clean and Lightweight
  - Stories Links screenshots
    - Can be disabled (will not be loaded)
    - WebP and PNG files are generated for each screenshot. WebP will be used if your browser supports them
  - Simple HTML and CSS pages
  - No extra web frameworks
  - No Javascript scripts
- Deployed via GitHub Actions

## Use the public online version

Every day a [GitHub workflow](https://github.com/lopespm/hackernews-daily/actions) is run, which deploys the results to a publicly available GitHub page at: [https://lopespm.github.io/hackernews-daily](https://lopespm.github.io/hackernews-daily)


## Local usage

**Step 1** Clone this repository:

```bash
$ git clone https://github.com/lopespm/autocomplete.git
```

**Step 2 (optional, but recommended)** Create a virtual environment:

```bash
$ python3 -m venv env
$ source env/bin/activate
```

**Step 3** Install required packaged

```bash
$ pip install -r requirements.txt
```

**Step 4** Run - this will create/update the best hacker news stories, and generate the web pages and screenshots:

```bash
$ python3 main.py
```

**Step 5** The generated web pages and screenshots will placed in the `generated` local folder. Open one of the generated web pages in your browser, such as `generated/index.html`


## Page Load Benchmark

Measurements taken in late December 2020 (all downloaded resources taken into account):
- "Latest" without screenshots: about 18 KB
- "Latest" with screenshots: about 160 KB
- "All" without screenshots: about 109 KB
- "All" with screenshots: about 1220 KB
