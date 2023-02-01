def change_format(show):
    show['rating'] = str(show['rating'])[:3]
    show['year'] = str(show['year'])[:4]
    avg_runtime = show['avg_runtime']
    hours = int(avg_runtime // 60)
    minutes = int(avg_runtime % 60)
    show['avg_runtime'] = f'{hours}h {minutes}min' if hours > 0 else f'{minutes}min'
    print(show['trailer'])
    show['trailer'] = str(show['trailer'])[27:]
    print(show['trailer'])
    return show
