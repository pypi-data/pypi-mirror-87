import click


def duck_art():
    duck = """
            ,----,
       ___.`      `,
       `===  D     :
         `'.      .'
            )    (                   ,
           /      \_________________/|
          /                          |
         |                           ;
         |               _____       /
         |      \       ______7    ,'
         |       \    ______7     /
          \       `-,____7      ,'   
    ^~^~^~^`\                  /~^~^~^~^
      ~^~^~^ `----------------' ~^~^~^
     ~^~^~^~^~^^~^~^~^~^~^~^~^~^~^~^~
    """
    return duck


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--name', default='', help='Who are you?')
def cli(verbose, name):
    click.echo(duck_art())
    click.echo("Hello World. Welcome to PyNevin's CEG CLI")
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo('Bye {0}'.format(name))
