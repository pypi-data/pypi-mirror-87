# Espresso IR

## Introduction

Espresso IR provides the fuctionality to automate memory aquisitions of Windows based EC2 instances and stores them in an S3 bucket. Currently it uses DumpIt to facilitate the memory aquisition part but with some minor edits you could use your tool of choice.

## Getting Started

use  `pip install espresso_ir` to install the module.

GitHub repositiory <https://github.com/Terrizmo/espresso_ir>

## Requirements

You must have an account with programatic access to your AWS environment. Once you have the access-key-id and secret-access-key. Use `aws configure` to store these in your home directory. These details will then be used each time your run an espresso_ir command.

This tool has been designed to use [DumpIt](https://blog.comae.io/your-favorite-memory-toolkit-is-back-f97072d33d5c) by comae. Other memory acquisition tools may be availible in the future.

Finally System manager must be able to communicate with the system manager agent on the EC2 instances you wish to acquire the memory from. You can create the necessary role with the required policies with this tool,  `--setup` flag. Note if you add this role after the the system manager agent has turned on you will need to reboot the agent or the instance to get this functionality. **Rebooting the EC2 instance will lose artifacts in memory, proabably all of them!**

Include essential instructions for:

- Installing It
- Configuring It
- Running it

## TODO

- Next steps
- Features planned
- Known bugs (shortlist)

## Contact

- Email address
- Google Group/mailing list (if applicable)
- IRC or Slack (if applicable)
