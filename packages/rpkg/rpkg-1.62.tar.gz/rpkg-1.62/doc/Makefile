# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXBUILD   = sphinx-build-3
SPHINXPROJ    = rpkg
SOURCEDIR     = source
BUILDDIR      = build


all: clean-command-docs generate-man-pages-list html man
.PHONY: all

clean-files:
	@rm -f "$(SOURCEDIR)/commands/*.rst"
	@rm -f $(SOURCEDIR)/cli.rst
.PHONY: clean-files

clean-man-pages:
	@rm -rf "$(BUILDDIR)/man/"
.PHONY: clean-man-pages

generate-man-pages-list:
	@python3 generate_commands_docs.py
.PHONY: generate-man-pages-list

man: clean-man-pages
	@$(SPHINXBUILD) -b man "$(SOURCEDIR)" "$(BUILDDIR)/man/"
.PHONY: man

html: clean-files generate-man-pages-list
	@$(SPHINXBUILD) -E -b html "$(SOURCEDIR)" "$(BUILDDIR)/html/"
.PHONY: html
