FROM kitware/trame:py3.10-glvnd-2024-09
COPY --chown=trame-user:trame-user ./docker /deploy
ENV NRTK_EXPLORER_NUM_IMAGES=16
RUN mv /deploy/config/apache/001-trame.tpl /opt/trame/apache.tpl
RUN /opt/trame/entrypoint.sh build
