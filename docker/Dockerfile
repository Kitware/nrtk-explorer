FROM kitware/trame:py3.10-glvnd-2024-09
COPY --chown=trame-user:trame-user ./docker /deploy
RUN /opt/trame/entrypoint.sh build
