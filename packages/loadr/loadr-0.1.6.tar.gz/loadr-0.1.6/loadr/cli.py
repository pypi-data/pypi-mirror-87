import os
from datetime import datetime
import random
import yaml
import requests
import urllib3
import click
from jinja2 import Template
from faker import Faker

from loadr import __version__

urllib3.disable_warnings()

@click.group()
@click.version_option(version=__version__)
def main():
    pass

@main.command(name='generate')
@click.option('-c', '--count', type=click.IntRange(0, 9999, clamp=True), help="Number of files to generate", default=1)
@click.option('-t', '--template', type=click.Path(exists=True), help="Path to template", required=True)
@click.option('--vars', type=click.Path(exists=True), help="Path to variables")
@click.option('-o', '--output', type=click.Path(exists=False, file_okay=False, resolve_path=True), help="Output directory", default=os.path.join(os.getcwd(), 'output'))
def generate(count, template, vars, output):
    """
    Generate file(s) using jinja2 template.
    """
    if not os.path.exists(output):
        os.makedirs(output)

    name = template.split(os.path.sep)[-1]

    # Check template extension (expecting '.jinja2')
    if not name.split('.')[-1] == 'j2':
        raise click.ClickException(f"{template} is not a '.j2' template 😔")
    
    filename = name.split('.')[:-1]

    Faker.seed(0)

    try:
        with open(template) as f:
            jt = Template(f.read())

        params = dict(
            date     = datetime.now().strftime('%Y-%m-%d'), 
            datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            random   = random.randrange(1,100),
            fake     = Faker(["nl_NL"])
        )

        if vars:
            static = dict()

            with open(vars, 'r') as f:
                try:
                    static = yaml.safe_load(f)
                except yaml.parser.ParserError:
                    raise click.ClickException(f'{vars} could not be parsed.')
                except yaml.scanner.ScannerError as e:
                    raise click.ClickException(f'loading yaml\n\n{str(e)}')

            params.update(dict(vars=static))

        for i in range(count):
            jt.stream(**params).dump(os.path.join(output,f"{'.'.join(filename[:-1])}-{format(i+1, '03')}.{filename[-1]}"))

        click.echo(f'Finished generating {count} file(s) in directory {output} 🤖')

    except Exception as e:
        raise click.ClickException(f'generating templates\n\n{repr(e)}')

@main.command(name='post')
@click.option('-i', '--input', type=click.Path(exists=True, resolve_path=True), help="Input path. Can be either file or directory.", required=True)
@click.option('-u', '--url', help="URL to post to." , required=True)
@click.option('--verify/--no-verify', help="Host SSL certificate verification.", default=False)
@click.option('--debug', is_flag=True, default=False)
def post(input, url, verify, debug):
    """
    Upload files to URL
    """
    click.secho(f'Start uploading file(s) to {url}', bold=True)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': f'loadr/{__version__}'
    }
    if os.path.isdir(input):
        files   = sorted(os.listdir(input)) 
        basedir = input
    elif os.path.isfile(input):
        files   = [os.path.basename(input)]
        basedir = os.path.dirname(input)
    else:
        raise click.ClickException(f"Invalid input '{input}'")

    with click.progressbar(length=len(files), label=click.style(f'Uploading {len(files)} file(s)', bold=True), fill_char=click.style("#", bold=True)) as _progress:
        for i, filename in enumerate(files):
            try:
                _progress.update(i)
                with open(os.path.join(basedir, filename), 'r') as f:
                    r = requests.post(url, data=f, headers=headers, verify=verify, allow_redirects=True)

                r.raise_for_status()

            except Exception as e:
                raise click.ClickException(f'uploading files\n\n{repr(e)}')

    click.secho('Finished upload 🤖', bold=True)

if __name__ == '__main__':
    main()