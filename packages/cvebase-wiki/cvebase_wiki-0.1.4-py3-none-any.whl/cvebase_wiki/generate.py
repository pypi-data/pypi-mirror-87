import click


@click.command()
@click.option(
    '-t',
    '--type',
    type=click.Choice(['researcher'], case_sensitive=False)
)
@click.option(
    '-r',
    '--repo',
    type=click.Path(exists=True),
    help='path to cvebase.com repo'
)
def generate(type, repo):
    """Generate new TYPE of file"""
    if type == 'researcher':
        r = setup_researcher()
        # outpath = compile_researcher_md(repo, r)
        # print(f"Generated researcher profile: {outpath}")


def setup_researcher():
    click.echo("\nEnter required fields:\n")

    r = {}
    r['name'] = click.prompt('Name')
    r['alias'] = click.prompt('Alias')
    cves = click.prompt('CVEs (if multiple, separate by space)')
    r['cves'] = cves.split()

    click.echo("\nEnter/skip optional fields:\n")

    if (data := click.prompt('Researcher nationality (alpha-2 country code)', default='us', type=str)) != '':
        r['nationality'] = data

    if (data := click.prompt('Website URL (include http/https)', default='')) != '':
        r['website'] = data

    if (data := click.prompt('Twitter username (without @)', default='')) != '':
        r['twitter'] = data

    if (data := click.prompt('GitHub username', default='')) != '':
        r['github'] = data

    if (data := click.prompt('Linkedin username (linkedin.com/in/<username>)', default='')) != '':
        r['linkedin'] = data

    if (data := click.prompt('Short bio', default='')) != '':
        r['bio'] = data

    return r