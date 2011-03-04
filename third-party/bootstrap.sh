#!/bin/sh

SRCDIR='src'
WEBOB='1.0.3'
SQLA='0.6.6'

if [ -d $SRCDIR ] 
then
    rm -rf ./$SRCDIR
    rm insanities
    rm mage
    rm mint.py
    rm memcache.py
fi

mkdir $SRCDIR
cd $SRCDIR

git clone git://github.com/riffm/insanities-testing.git
git clone git://github.com/riffm/mage.git
git clone git://github.com/riffm/mint.git
git clone git://github.com/riffm/python-memcached.git

cd ..

ln -s ./$SRCDIR/insanities-testing/insanities ./
ln -s ./$SRCDIR/mage/mage ./
ln -s ./$SRCDIR/mint/mint.py ./
ln -s ./$SRCDIR/python-memcached/memcache.py ./


WEBOBDIR="WebOb-$WEBOB"
if [ ! -d  $WEBOBDIR ]
then
    curl http://pypi.python.org/packages/source/W/WebOb/WebOb-$WEBOB.tar.gz#md5=808066a82e8ba4f0501cc6550f8878a7 | tar -xz
    ln -s ./$WEBOBDIR/webob ./
fi

SQLADIR="SQLAlchemy-$SQLA"
if [ ! -d  $SQLADIR ]
then
    curl http://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-$SQLA.tar.gz#md5=359f02242c52e92aa881c36c8e3720d8 | tar -xz
    ln -s ./$SQLADIR/lib/sqlalchemy ./
fi
