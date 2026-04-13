from __future__ import annotations

import sys

from app import create_app
from app.extensions import db
from app.seed import seed_demo_data


app = create_app()


def init_db(force: bool = False) -> None:
    with app.app_context():
        if force:
            db.drop_all()
        db.create_all()
        seed_demo_data(force=False)
        print('Database initialized and demo data loaded.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'init-db':
            init_db(force=False)
        elif command == 'reset-db':
            init_db(force=True)
        elif command == 'seed-demo':
            with app.app_context():
                seed_demo_data(force=False)
                print('Seed completed.')
        else:
            raise SystemExit(f'Unknown command: {command}')
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
