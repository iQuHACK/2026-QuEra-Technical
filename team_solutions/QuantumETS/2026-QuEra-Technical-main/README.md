# iQuHACK 2026 - QuEra Challenge

> Give me an AOD large enough and I can move the atoms of the world. - *John Long, Scientific Software Engineer @ QuEra*

So you fancy taking on QuEra's technical challenge for iQuHack 2026?! We welcome you with open arms!

Here you will learn all the details about the challenge, and needed to operate QuEra resources for iQuHack 2026. 


## Contents
This repo contains everything you need to get going. Mainly:

- [`challenge.md`](challenge.md) contains the challenge statement, with directions and guidelines
- Inside the `assets` folder you'll find
  - slide decks expanding on the topics from the Friday tutorial, including some basic information about error correction
  - images of interest that summarize the circuits you will be studying
  - a cheat sheet with methods and processes in Bloqade you may find useful
- [`project.toml`](project.toml) is a configurational file from which you can easily recover all packages needed for the challenge, in their correct version
  

## Coding Infrastructure

This challenge will get you started with basic knowledge to use QuEra's upcoming gate-based, error-correction-focused, hardware. For so, you will be operating on our SDK [Bloqade](https://bloqade.quera.com/latest/digital/), using efficient libraries for the simulation of stabilizer circuits like Stim and our recently launched library [Tsim](https://queracomputing.github.io/tsim/dev/). 

To get the minimal packages installed all you have to do is make use of [`project.toml`](project.toml) as follows:


### Setup (Python + `uv`)

**1) Install `uv`**
- **macOS / Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh

* **Windows (PowerShell):**
  ```powershell
  irm https://astral.sh/uv/install.ps1 | iex
  ```

Verify:
```bash
uv --version
```

**2) Install dependencies from the provided TOML**

From the project folder (where the TOML lives):

```bash
# create and sync virtual environment according to toml
uv sync
# activate it
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows (PowerShell)

```

With the above, you can just create python scripts and notebooks for your solution and run from the same folder where your new environment is. You will have the minimal infrastructure with which we can guarantee you can create meaningful solutions to the challenge! Still, you are welcome to bring other packages and software of your interest, if they can help you with your unique solutions! 


## Resource Availability and Code of Conduct

There is no access to quantum hardware for this challenge. The challenge is designed to be solved using the Bloqade SDK for digital neutral atom quantum computers.

**As for technical requirements, we expect:**

- all your circuits should be made using Bloqade, in particular Squin kernels.
- simulation backends allowed include PyQrack, Stim, or Tsim. Tthe latter two providing access much bigger sizes for Clifford-only situations or with small amounts of magic, respectively.

We encourage you pay particular attention to using Tsim, as you have early access to it here at this iQuHack challenge! Tsim is QuEra's new efficient backend sampler for circuits with Pauli noise and small amounts of magic. Like Stim, Tsim is based on stabilizer formalism to achieve ultimate speed and volume capacity. With Tsim, you can have access to better circuit plotting capabilities, more flexibility to deal with encoding rounding errors. But above everything, you can add small amounts of magic (like T gates) to the circuit while still being able to perform simulations with tens and tens of qubits! This should give you a lot of flexibility to explore different phenomena in your solutions.


## Documentation

This year’s iQuHACK challenges require a write-up/documentation portion that is heavily considered during judging. The write-up is a chance for you to be creative in describing your approach and describing your process, as well as presenting the performance of your solutions. It should clearly explain the problem, the approaches you used, and your implementation with results.

Make sure to clearly link the documentation into the `README.md` of your own solutions folder and to include a link to the original challenge repository from the documentation!


## Submission

To submit the challenge, do the following:
1. Place all the code you wrote in one folder with your team name under the `team_solutions/` folder (for example `team_solutions/quantum_team`).
2. Create a new entry in `team_solutions.md` with your solution and your documentation. Your solution shuold contain a python script that runs your solution and  a `.pdf` of your presentation slides. Make sure to add an updated TOML file in case you are using extra packages needed to run your solution.
3. Create a Pull Request from your repository to the original challenge repository
4. Submit the "challenge submission" form as required by iQuHack organization

Project submission forms will automatically close on Sunday at 10am EST and won't accept late submissions.

## Evaluation criteria

This is a technical challenge, but we try to keep it a bit open ended to allow teams to explore their interests and make use of their main strengths. To help guide your efforts, here are some points we will take into account when evaluating your work:

- How well are you using Bloqade’s kernels to generate circuits and noise models.
- How accurate are your analyses of error sources via both heuristic and bespoke noise models and shuttling schedules
- How detailed was your analysis of the error detection/correction process. Did you succeed at making it work? If not, why?
- How smart has been your compilation of moves and syndrome extraction process? Choice of layout, choice of static and moving registers, etc
- How far could you push your simulations? Did you achieve extensive calculations using smart implementations or use of parallelism?
