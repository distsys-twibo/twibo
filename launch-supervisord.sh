#!/bin/bash

exec supervisord -c `pwd`/supervisord.conf
