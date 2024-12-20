# User Instructions

Welcome to the Agentic Starter Kit.

The idea behind this repo is to give developers working with tools like
Windsurf or Cline a way to manage context and keep models/agents on the right
track.

## Setup

1. Start with ChatGPT (or yourself) to flesh out an overview of your project.
   Drop that into [design overview](./agent/design/overview.md)
2. Work with your model to document/update the [tech
   stack](/agent/design/tech-stack.md) (which is seeded with information for my
python project preferences)
3. Then work with your model to perform the task of filing out the
   [deliverables](/agent/design/deliverables.md) based on the overview and the
tech stack.

## Development

1. I like to manage python and environments myself with `uv` - so make a new repo, then `uv init` and either make a `requirements.txt` file or start using `uv add` to add requirements.
2. I also typically manage docker myself without letting the Agent run docker commands - this repo comes with a dockerfile, compose file, and entrypoint script to serve as fodder for the docker setup
