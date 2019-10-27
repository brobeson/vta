Tool Configuration
==================
VTA can be configured via a YAML file. This allows specifying VTA's behavior in
an easily repeatable manner. Write a YAML file, and specify it with the command
option ``--configuration FILE``. Here are the options that can be specified.

:loss: The parent option for configuring the ``vta loss`` command.

loss
----
:line_loss: (boolean) If ``true``, draw line graphs of the loss data.
:line_precision: (boolean) If ``true``, draw line graphs of the precision data.
:scatter_loss: (boolean) If ``true``, draw loss data as a scatter plot. This
               will also draw points on the line graph if ``line_loss`` is
               ``true``.
:scatter_precision: (boolean) If ``true``, draw precision data as a scatter
                    plot. This will also draw points on the line graph if
                    ``line_precision`` is ``true``.
