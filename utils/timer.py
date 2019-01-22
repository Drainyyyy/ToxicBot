from discord.ext import commands
#   Used for later projects like a reminder... all WIP and coming soon.
time_specs = {
    "d": 86400,
    "h": 3600,
    "m": 60,
    "s": 1
}


def get_count(count):
    count_spec = count[len(count) - 1:]
    time = count[:len(count) - 1]
    if count_spec in time_specs and time.isdigit():
        count_sec = int(time) * time_specs[count_spec]
        return count_sec
    else:
        raise commands.UserInputError("Invalid syntax.\nTime must be specified as [count][d, h, m, s]")
