#!/bin/bash
sass ./static/scss/base.scss:./static/css/base.css --style compressed
sass ./static/scss/blog.scss:./static/css/blog.css --style compressed
sass ./static/scss/blogs.scss:./static/css/blogs.css --style compressed
sass ./static/scss/sources.scss:./static/css/sources.css --style compressed
sass ./static/scss/resources.scss:./static/css/resources.css --style compressed
sass ./static/scss/about.scss:./static/css/about.css --style compressed