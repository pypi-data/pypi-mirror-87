# -*- coding: utf-8 -*-

from fastapi import APIRouter

from service.base import DataSource


router = APIRouter()


@router.get(r'/')
async def default():

    return DataSource().online


@router.get(r'/health')
async def default():

    return await DataSource().health()
