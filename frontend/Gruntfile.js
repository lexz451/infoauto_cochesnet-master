module.exports = function(grunt) {

	// Project configuration.
	grunt.initConfig({
		nggettext_extract: {
			pot: {
				files: {
					'po/template.pot': ['**/*.html','src/app/**/*.js']
				}
			}
		},
		nggettext_compile: {
			all: {
				files: {
					'src/app/translations.js': ['po/*.po']
				}
			}
		}
	});

	grunt.loadNpmTasks('grunt-angular-gettext');

};