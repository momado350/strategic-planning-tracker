
import os
import sys

from flask import jsonify

from app import create_app
from app.extensions import db
from app.seed import seed_demo_data


app = create_app()


@app.get('/healthz')
def healthz():
    return jsonify({'ok': True}), 200


def init_db(force: bool = False) -> None:
    with app.app_context():
        db.create_all()
        seed_demo_data(force=force)
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
        port = int(os.getenv('PORT', '5000'))
        app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')
