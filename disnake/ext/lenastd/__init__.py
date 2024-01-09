# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

import disnake
from disnake.ext import commands

__version__ = "0.1.0a1"

__all__ = ("app_command_id",)

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    InvokableSlashCommand: TypeAlias = """(
        commands.InvokableSlashCommand
        | commands.SubCommand
        | commands.SubCommandGroup
    )"""

    InvokableAppCommand: TypeAlias = """(
        InvokableSlashCommand
        | commands.InvokableMessageCommand
        | commands.InvokableUserCommand
        | commands.InvokableApplicationCommand
    )"""


def app_command_id(
    client: disnake.Client,
    command: InvokableAppCommand,
    *,
    guild_id: int | None = None,
) -> int | None:
    """Retrieve application command ID from ``client``'s cache.

    Parameters
    ----------
    client: :class:`disnake.Client`
        The client to use for retrieving API commands.
    command: InvokableAppCommand
        A command created using one of the decorators found in :module:`disnake.ext.commands`.
    guild_id: :class:`int` | :class:`None`
        An optional guild to search the command in, if it's not global.

    Returns
    -------
    :class:`int` | :class:`None`
        The command's ID, if available.
    """
    if isinstance(command, InvokableSlashCommand):
        cmdtype = disnake.ApplicationCommandType.chat_input
    elif isinstance(command, commands.InvokableMessageCommand):
        cmdtype = disnake.ApplicationCommandType.message
    elif isinstance(command, commands.InvokableUserCommand):
        cmdtype = disnake.ApplicationCommandType.user
    else:
        raise TypeError(f"Unknown application command type: {command!r}")

    cmdname = command.qualified_name.split()[0]

    if command.guild_ids:
        if not guild_id:
            raise ValueError("`cmd` is a guild command, but `guild_id` was not specified.")

        api_cmd = client.get_guild_command_named(guild_id, cmdname, cmdtype)
    else:
        api_cmd = client.get_global_command_named(cmdname, cmdtype)

    return api_cmd and api_cmd.id
