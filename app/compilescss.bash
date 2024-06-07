#!/bin/bash
sass ./static/scss/base.scss:./static/css/base.css --style compressed
sass ./static/scss/blog.scss:./static/css/blog.css --style compressed
sass ./static/scss/blogs.scss:./static/css/blogs.css --style compressed
