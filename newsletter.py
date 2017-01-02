import click

from subscribah import Subscriber, mail, app


@click.command(name='newsletter')
@click.option('--subject', prompt=True)
@click.argument('message', type=click.Path(exists=True))
def main(message, subject):
    subscribers = Subscriber.query.filter_by(verified=True)

    if not click.confirm(
        'Send "{}" to {} subscriber(s)?'.format(subject, subscribers.count())
    ):
        click.echo('By then')
        exit(1)

    message = open(message).read()

    with app.app_context():
        with mail.connect() as conn:
            with click.progressbar(subscribers) as subscribers:
                for subscriber in subscribers:
                    subscriber.send_newsletter_email(subject, message, conn)

    click.echo('Done!')


if __name__ == '__main__':
    main()
