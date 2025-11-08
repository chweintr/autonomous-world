# How to Set Your OpenAI API Key

You have **two simple options**. Choose one:

---

## ✅ OPTION 1: Direct in Terminal (Easiest)

Just paste this in your terminal and replace with your key:

```bash
export OPENAI_API_KEY="sk-your-actual-key-here"
```

**That's it!** Now run:
```bash
python3 test_llm.py
```

**Note:** This only lasts until you close the terminal.

---

## ✅ OPTION 2: Make It Permanent

Add to your shell config so it's always available:

```bash
echo 'export OPENAI_API_KEY="sk-your-actual-key-here"' >> ~/.zshrc
source ~/.zshrc
```

Now it's set forever (or until you change it).

---

## 🔍 Check If It's Set

Run this to verify:

```bash
echo $OPENAI_API_KEY
```

Should show your key (starting with `sk-`).

---

## 🧪 Test the Connection

```bash
cd /Volumes/T7/Sandbox/autonomous-world
python3 test_llm.py
```

If it says "✓ LLM Integration Ready!" you're good to go!

---

## 🚀 Run the System

```bash
python3 run.py
```

Open http://localhost:5000 and check "Use LLM for descriptions"

---

## 🔑 Where to Get Your Key

https://platform.openai.com/api-keys

1. Sign in
2. Click "Create new secret key"
3. Copy it (starts with `sk-`)
4. Paste it in the command above

---

## ❓ Still Stuck?

Just run this and paste your key when prompted:

```bash
read -p "Paste your OpenAI API key: " key
export OPENAI_API_KEY="$key"
python3 test_llm.py
```

This will set it for the current session and test it immediately.

