#!/bin/bash

mkdir dumps

redis-server ./redis.conf
redis-server ./redis-lru.conf