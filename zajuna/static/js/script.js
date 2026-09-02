tailwind.config = {

            darkMode: "class",

            theme: {

                extend: {

                    colors: {

                        "outline-variant": "#d9c3af",
                        "on-primary-fixed-variant": "#683d00",
                        "error": "#ba1a1a",
                        "on-tertiary": "#ffffff",
                        "error-container": "#ffdad6",
                        "link-accent": "#18A0FB",

                        "surface-container-low": "#f3f3f3",
                        "on-primary-fixed": "#2c1700",

                        "secondary": "#7b5800",
                        "on-secondary": "#ffffff",

                        "tertiary-fixed": "#f7e37a",

                        "surface": "#f9f9f9",

                        "on-primary-container": "#5d3600",

                        "on-tertiary-container": "#483f00",

                        "on-error": "#ffffff",

                        "inverse-primary": "#ffb86a",

                        "on-secondary-fixed-variant": "#5d4200",

                        "on-background": "#1b1b1b",

                        "surface-container-highest": "#e2e2e2",
                        "surface-container-high": "#e8e8e8",

                        "primary-fixed": "#ffdcbc",
                        "secondary-fixed": "#ffdea4",

                        "on-secondary-fixed": "#261900",

                        "primary-fixed-dim": "#ffb86a",

                        "on-surface": "#1b1b1b",

                        "tertiary-container": "#bcab48",

                        "surface-container-lowest": "#ffffff",

                        "surface-container": "#eeeeee",

                        "on-primary": "#ffffff",

                        "primary": "#885200",

                        "background-page": "#FFFCE2",

                        "secondary-container": "#febf31",

                        "on-surface-variant": "#534435",

                        "surface-soft": "#F2F2F2",

                        "on-tertiary-fixed-variant": "#514700",

                        "inverse-surface": "#303030",

                        "surface-dim": "#dadada",

                        "background": "#f9f9f9",

                        "primary-container": "#ed9726",

                        "surface-tint": "#885200",

                        "tertiary": "#6c5e00",

                        "secondary-fixed-dim": "#fabc2e",

                        "outline": "#867463",

                        "on-secondary-container": "#6e4f00",

                        "inverse-on-surface": "#f1f1f1",

                        "on-tertiary-fixed": "#211c00",

                        "surface-variant": "#e2e2e2"
                    },


                    borderRadius: {

                        DEFAULT: "0.125rem",
                        lg: "0.25rem",
                        xl: "0.5rem",
                        full: "0.75rem"

                    },


                    spacing: {

                        "container-max": "1200px",
                        "base": "8px",
                        "gutter": "24px",
                        "margin-mobile": "16px",
                        "margin-desktop": "64px"

                    },


                    fontFamily: {

                        "headline-lg-mobile": ["Libre Caslon Text"],
                        "headline-lg": ["Libre Caslon Text"],
                        "label-sm": ["Inter"],
                        "label-md": ["Inter"],
                        "display-lg": ["Libre Caslon Text"],
                        "body-md": ["Source Serif 4"],
                        "headline-md": ["Libre Caslon Text"],
                        "body-lg": ["Source Serif 4"]

                    },


                    fontSize: {

                        "headline-lg-mobile": [
                            "28px",
                            {
                                lineHeight: "36px",
                                fontWeight: "700"
                            }
                        ],

                        "headline-lg": [
                            "32px",
                            {
                                lineHeight: "40px",
                                fontWeight: "700"
                            }
                        ],

                        "label-sm": [
                            "12px",
                            {
                                lineHeight: "16px",
                                fontWeight: "600"
                            }
                        ],

                        "label-md": [
                            "14px",
                            {
                                lineHeight: "20px",
                                letterSpacing: "0.01em",
                                fontWeight: "500"
                            }
                        ],

                        "display-lg": [
                            "48px",
                            {
                                lineHeight: "56px",
                                letterSpacing: "-0.02em",
                                fontWeight: "700"
                            }
                        ],

                        "body-md": [
                            "16px",
                            {
                                lineHeight: "24px",
                                fontWeight: "400"
                            }
                        ],

                        "headline-md": [
                            "24px",
                            {
                                lineHeight: "32px",
                                fontWeight: "600"
                            }
                        ],

                        "body-lg": [
                            "18px",
                            {
                                lineHeight: "28px",
                                fontWeight: "400"
                            }
                        ]

                    }

                }

            }

        };