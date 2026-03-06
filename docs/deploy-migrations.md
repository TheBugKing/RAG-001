# Running migrations in deployment

Alembic migrations are **not** run automatically when the app starts in production. Run them once per deployment as below.

## 1. Container / Azure App Service (entrypoint – recommended)

The image uses `scripts/entrypoint.sh` as the default command. Migrations run **only when `RUN_MIGRATIONS` is set**.

- **Production (App Service):** In the container’s environment, set `RUN_MIGRATIONS=true` (or `1`). On start, the entrypoint runs `alembic upgrade head` then starts the app.
- **Local `docker run`:** Do **not** set `RUN_MIGRATIONS`. The entrypoint skips migrations and starts the app. No risk of running migrations against a local or shared DB by mistake.

Same image everywhere; behavior is controlled by the env var.

**Option B – Separate migration job**  
Run a one-off container with the same image and env, but override the command:

```bash
docker run --rm -e DATABASE_URL="..." your-image alembic upgrade head
```

Then start the app container as usual. In Azure App Service you can run the migration as a separate "job" or during a deployment slot swap.

## 2. CI/CD (GitHub Actions, Azure DevOps, etc.)

Add a step that runs migrations against the **deployment** database **before** or **as part of** release:

```yaml
# Example: GitHub Actions
- name: Run migrations
  run: alembic upgrade head
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

Or call the script:

```yaml
- name: Run migrations
  run: ./scripts/run_migrations.sh
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

Ensure the job has the same `DATABASE_URL` (and any other env) that the app will use. Run this step once per deployment (e.g. after deploy to staging/prod), not on every developer push to main.

## 3. Local development

To run migrations automatically when you start the app locally, set:

```bash
RUN_MIGRATIONS=true
```

in your `.env`. Leave it unset or `false` in production so only the CI/CD or entrypoint runs migrations.
