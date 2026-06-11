# 📤 GitHub Upload Guide
## IoT Vehicle Tracking & Geofence Threat Prevention System

This guide walks you through publishing your project to GitHub from scratch — whether you are uploading for the first time or pushing updates to an existing repo.

---

## ✅ Pre-flight Checklist

Before touching Git, confirm the following:

- [ ] `dashboard/config.json` is listed in `.gitignore` and is **not tracked** by Git
- [ ] `dashboard/` folder does NOT appear in `git status` output
- [ ] `.venv/` is in your `.gitignore`
- [ ] `__pycache__/` is in your `.gitignore`
- [ ] No duplicate internal folders remain in the repo
- [ ] `data/location_history.csv` contains at least one simulation run
- [ ] `outputs/reports/route_incident_report.pdf` has been generated
- [ ] `README.md` is in the project root
- [ ] ThingSpeak Write API key has been rotated if `config.json` was ever previously committed

Your `.gitignore` should contain at minimum:

```
dashboard/config.json
dashboard/
.venv/
__pycache__/
*.pyc
*.pyo
.DS_Store
Thumbs.db
```

> 🔒 **Why `dashboard/` is git-ignored:** This folder holds `config.json` which contains your ThingSpeak Write API key. It was identified as a sensitive path during development and is fully excluded from version control. The folder must be recreated manually after any fresh clone.

---

## 🔧 Part 1 — One-Time Setup (First Upload)

### Step 1: Install Git

Check if Git is already installed:

```bash
git --version
```

If not installed, download from: https://git-scm.com/downloads

### Step 2: Configure Git Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Step 3: Create the GitHub Repository

1. Go to https://github.com and log in
2. Click the **+** icon (top-right) → **New repository**
3. Fill in:
   - **Repository name:** `iot-vehicle-tracker`
   - **Description:** `IoT Vehicle Tracking & Geofence Threat Prevention System using Python, ThingSpeak, and MATLAB`
   - **Visibility:** Public ✅ (for portfolio visibility)
   - **DO NOT** tick "Add a README file" — you already have one
4. Click **Create repository**
5. Copy the HTTPS URL shown (e.g. `https://github.com/<your-username>/iot-vehicle-tracker.git`)

---

## 🚀 Part 2 — Initial Push

Run these commands from inside your project folder (`iot-vehicle-tracker/`):

### Step 1: Initialise Git

```bash
git init
```

### Step 2: Stage All Files

```bash
git add .
```

### Step 3: Verify What Is Being Committed

```bash
git status
```

Confirm the following are listed as **tracked** (green):
```
python_simulation/simulation_engine.py
data/location_history.csv
outputs/reports/route_incident_report.pdf
README.md
.gitignore
```

Confirm the following are **NOT** listed (should be ignored):
```
dashboard/              ← must NOT appear (entire folder is git-ignored)
dashboard/config.json   ← must NOT appear
.venv/                  ← must NOT appear
__pycache__/            ← must NOT appear
```

> ⛔ If `dashboard/config.json` or the `dashboard/` folder appears in the staged list, **stop immediately.**
> Run the following before continuing:
> ```bash
> git rm -r --cached dashboard/
> ```
> Then add `dashboard/` to your `.gitignore`, commit, and push. After that, **rotate your ThingSpeak Write API key** at https://thingspeak.com — the old key must be considered compromised.

### Step 4: Create the First Commit

```bash
git commit -m "feat: initial release — IoT vehicle tracker with geofence engine and ThingSpeak cloud dashboard"
```

### Step 5: Set the Branch Name

```bash
git branch -M main
```

### Step 6: Link to GitHub

Replace `<your-username>` with your actual GitHub username:

```bash
git remote add origin https://github.com/<your-username>/iot-vehicle-tracker.git
```

### Step 7: Push to GitHub

```bash
git push -u origin main
```

You will be prompted to authenticate. Use your GitHub username and a **Personal Access Token** (not your password — see note below).

---

## 🔑 GitHub Authentication — Personal Access Token (PAT)

GitHub no longer accepts passwords for Git operations. You need a PAT.

1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Give it a name (e.g. `iot-tracker-upload`)
4. Set expiry (90 days is fine for portfolio work)
5. Tick the **repo** scope (full repository access)
6. Click **Generate token**
7. **Copy the token immediately** — it is only shown once

When Git prompts for a password, paste the token.

To avoid re-entering it every push, store it via Git credential manager:

```bash
git config --global credential.helper store
```

---

## 🔄 Part 3 — Pushing Updates (Subsequent Commits)

After making changes to the project (e.g. running a new simulation, updating the README), push updates with:

```bash
# Stage changed files
git add .

# Review what changed
git status

# Commit with a clear message
git commit -m "chore: update location_history with new simulation run"

# Push
git push
```

### Recommended Commit Message Format

```
<type>: <short description>

Types:
feat     → new feature or capability
fix      → bug fix
chore    → data updates, dependency bumps, minor maintenance
docs     → README or documentation changes
refactor → code restructuring with no behaviour change
```

Examples:
```bash
git commit -m "feat: add speed threshold alerting to simulation engine"
git commit -m "docs: update README with ThingSpeak dashboard screenshots"
git commit -m "chore: regenerate route_incident_report for new Delhi test run"
```

---

## 🧹 Part 4 — Cleaning Up Duplicate Folders

If you previously pushed with duplicate internal folders, clean them with:

```bash
# Remove tracked folder from Git index (keeps local copy)
git rm -r --cached <duplicate-folder-name>/

# Commit the removal
git commit -m "chore: remove duplicate internal folder from tracking"

# Push the cleanup
git push
```

---

## 🚨 Part 5 — Emergency: If config.json Was Previously Committed

If `dashboard/config.json` was ever pushed to GitHub (even in a past commit), the API key inside it must be treated as compromised — deleting the file from the repo does **not** remove it from Git history.

**Take these steps in order:**

### 1. Remove from Git tracking

```bash
git rm -r --cached dashboard/
git commit -m "chore: remove dashboard/config.json from Git tracking — sensitive file"
git push
```

### 2. Rotate your ThingSpeak Write API Key immediately

1. Log in to https://thingspeak.com
2. Go to your channel → **API Keys** tab
3. Click **Generate New Write API Key**
4. Copy the new key
5. Update your local `dashboard/config.json` with the new key

> The old key is now invalid. Anyone who copied it from your commit history can no longer use it.

### 3. Confirm the folder is fully ignored

Add both lines to `.gitignore` if not already present:

```
dashboard/
dashboard/config.json
```

Then verify:

```bash
git status
# dashboard/ must not appear at all
```

### 4. Optional — Scrub full Git history

If you want to remove the file from all past commits (advanced):

```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch dashboard/config.json" \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

> ⚠️ Force-pushing rewrites history. Only do this on a personal repo where no one else has cloned. Since the key is already rotated, this step is optional but good hygiene.

---

## 🔍 Part 6 — Verifying on GitHub

After pushing, open your repository at:
```
https://github.com/<your-username>/iot-vehicle-tracker
```

Confirm:
- [ ] `README.md` renders correctly on the homepage with all badges
- [ ] `python_simulation/simulation_engine.py` is visible
- [ ] `data/location_history.csv` is visible
- [ ] `outputs/reports/route_incident_report.pdf` is visible and downloadable
- [ ] `dashboard/` folder does **NOT** appear anywhere in the file tree
- [ ] `dashboard/config.json` does **NOT** appear anywhere in the file tree
- [ ] No duplicate folders are present

---

## 🌐 Part 7 — Portfolio Optimisation (Optional but Recommended)

### Add a Repository Description and Tags

On the GitHub repo page:
1. Click the ⚙️ gear icon next to "About"
2. Add a description: `Real-time IoT vehicle tracking with Python digital twin, Haversine geofencing, ThingSpeak cloud telemetry, and MATLAB dashboard`
3. Add topics (tags): `iot`, `python`, `thingspeak`, `geofencing`, `vehicle-tracking`, `matlab`, `digital-twin`, `haversine`, `gps`, `cloud-iot`
4. Tick **Releases**, **Packages** off; tick **Website** if you have one

### Pin the Repository

1. Go to your GitHub profile: `https://github.com/<your-username>`
2. Click **Customize your profile**
3. Pin `iot-vehicle-tracker` as one of your featured repositories

---

## 🆘 Troubleshooting

| Problem | Fix |
|---|---|
| `fatal: remote origin already exists` | Run `git remote set-url origin <new-url>` |
| `error: src refspec main does not match any` | Run `git branch -M main` before pushing |
| `403 Forbidden` on push | Check your PAT is valid and has `repo` scope |
| `dashboard/config.json` was already pushed | Run `git rm -r --cached dashboard/`, commit, push; then **rotate your ThingSpeak Write API key immediately** at thingspeak.com → Channel → API Keys |
| `dashboard/` keeps reappearing in `git status` | Ensure both `dashboard/` and `dashboard/config.json` are in `.gitignore`, then run `git rm -r --cached dashboard/` again |
| Large file rejected | Add it to `.gitignore`, run `git rm --cached <file>`, and recommit |

---

*Guide prepared for: IoT Vehicle Tracking & Geofence Threat Prevention System*
