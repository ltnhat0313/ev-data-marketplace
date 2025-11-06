from __future__ import with_statement # PHẢI Ở DÒNG ĐẦU TIÊN
from logging.config import fileConfig
import os
import sys # Import sys
from pathlib import Path # Import Path

# Thêm thư mục gốc của dự án vào PYTHONPATH để Alembic có thể import 'app.*'
# Đây là vị trí chính xác: chạy trước các import từ 'app'
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app.core.database import Base # Dòng này giờ sẽ hoạt động
from app.models import models  # import models to register metadata
from app.core.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    # prefer env DATABASE_URL, fallback to alembic.ini
    return os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()