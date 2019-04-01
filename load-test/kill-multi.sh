#!/bin/bash

ps -ax | grep multi | grep -v grep | grep -v kill | awk '{print $1}' | xargs kill