"""Test app startup, window management, and feature routing in main.py."""

import unittest
from unittest.mock import MagicMock, patch

import main


class NoongarSeasonAppTests(unittest.TestCase):
    """Verify the app shell connects shared UI actions to feature controllers."""

    def test_initialization_configures_root_and_starts_security_flow(self):
        """Create controllers around the shared root and start authentication."""
        root = MagicMock()
        with (
            patch.object(main.NoongarSeasonApp, "_configure_styles"),
            patch.object(main, "SeasonWheel") as season_wheel,
            patch.object(main, "ClimatePage") as climate_page,
            patch.object(main, "QuestionPages") as question_pages,
            patch.object(main, "SourcePage") as source_page,
            patch.object(main, "SecurityModule") as security_module,
        ):
            app = main.NoongarSeasonApp(root)

        root.configure.assert_called_once_with(bg="#f4efe7")
        self.assertIsNone(app.current_frame)
        season_wheel.assert_called_once_with(app)
        climate_page.assert_called_once_with(app)
        question_pages.assert_called_once_with(app)
        source_page.assert_called_once_with(app)
        security_module.assert_called_once_with(app)
        app.security.show_startup_page.assert_called_once_with()

    def test_window_size_is_clamped_to_screen_bounds(self):
        """Shrink oversized windows and cap minimum size to the result."""
        root = MagicMock()
        root.winfo_screenwidth.return_value = 1000
        root.winfo_screenheight.return_value = 800
        app = main.NoongarSeasonApp.__new__(main.NoongarSeasonApp)
        app.root = root

        app.set_windowed_size("1200x900", (700, 600))

        root.geometry.assert_called_once_with("952x720")
        self.assertEqual(root.minsize.call_args_list[0].args, (1, 1))
        self.assertEqual(root.minsize.call_args_list[1].args, (700, 600))

    def test_window_size_preserves_requested_geometry_within_screen(self):
        """Keep requested dimensions when the display can accommodate them."""
        root = MagicMock()
        root.winfo_screenwidth.return_value = 1200
        root.winfo_screenheight.return_value = 900
        app = main.NoongarSeasonApp.__new__(main.NoongarSeasonApp)
        app.root = root

        app.set_windowed_size("800x600", (700, 540))

        root.geometry.assert_called_once_with("800x600")
        self.assertEqual(root.minsize.call_args_list[1].args, (700, 540))

    def test_clear_page_replaces_and_destroys_previous_frame(self):
        """Remove the old content frame and pack a newly created frame."""
        root = MagicMock()
        old_frame = MagicMock()
        new_frame = MagicMock()
        app = main.NoongarSeasonApp.__new__(main.NoongarSeasonApp)
        app.root = root
        app.current_frame = old_frame

        with patch.object(main.tk, "Frame", return_value=new_frame) as frame:
            app.clear_page()

        old_frame.destroy.assert_called_once_with()
        frame.assert_called_once_with(root, bg="#f4efe7")
        new_frame.pack.assert_called_once_with(fill="both", expand=True)
        self.assertIs(app.current_frame, new_frame)

    def test_sources_action_delegates_to_source_page(self):
        """Route the app-shell sources action to its feature controller."""
        app = main.NoongarSeasonApp.__new__(main.NoongarSeasonApp)
        app.source_page = MagicMock()

        app.show_sources_window()

        app.source_page.show_sources_window.assert_called_once_with()

    def test_climate_action_delegates_to_climate_page(self):
        """Route the app-shell climate action to its feature controller."""
        app = main.NoongarSeasonApp.__new__(main.NoongarSeasonApp)
        app.climate_page = MagicMock()

        app.show_climate_page()

        app.climate_page.show_climate_page.assert_called_once_with()

    def test_season_action_forwards_selected_name_to_wheel(self):
        """Preserve the selected season when routing to its detail page."""
        app = main.NoongarSeasonApp.__new__(main.NoongarSeasonApp)
        app.season_wheel = MagicMock()

        app.show_season_page("Makuru")

        app.season_wheel.show_season_page.assert_called_once_with("Makuru")

    def test_home_buttons_call_their_matching_actions(self):
        """Connect home-page buttons to wheel, sources, logout, and climate."""
        app = self._make_home_app()
        with (
            patch.object(main.tk, "Frame"),
            patch.object(main.tk, "Label"),
            patch.object(main.ttk, "Button") as button,
            patch.object(main, "display_question_results"),
        ):
            app.show_home_page()

        commands = {
            call.kwargs["text"]: call.kwargs["command"]
            for call in button.call_args_list
        }
        self.assertEqual(
            set(commands),
            {
                "Sources",
                "Open wheel of seasons",
                "Log out",
                "Explore 2024 climate data",
            },
        )
        commands["Sources"]()
        commands["Open wheel of seasons"]()
        commands["Log out"]()
        commands["Explore 2024 climate data"]()
        app.show_sources_window.assert_called_once_with()
        app.season_wheel.show_information_page.assert_called_once_with()
        app.security.show_login_page.assert_called_once_with()
        app.show_climate_page.assert_called_once_with()

    def test_home_page_passes_all_questions_to_the_question_renderer(self):
        """Provide both lookup prompts and FAQs with the question callback."""
        app = self._make_home_app()
        with (
            patch.object(main.tk, "Frame"),
            patch.object(main.tk, "Label"),
            patch.object(main.ttk, "Button"),
            patch.object(main, "display_question_results") as render_questions,
        ):
            app.show_home_page()

        results_frame, questions, callback = render_questions.call_args.args
        self.assertIs(results_frame, app.region_results)
        self.assertEqual(
            questions,
            (*main.REGION_QUESTIONS, *main.FAQ_ITEMS),
        )
        self.assertIs(callback, app.question_pages.show_question_page)

    @staticmethod
    def _make_home_app():
        """Build an app-shell instance with mocked feature controllers."""
        app = main.NoongarSeasonApp.__new__(main.NoongarSeasonApp)
        app.root = MagicMock()
        app.current_frame = None
        app.clear_page = MagicMock(
            side_effect=lambda: setattr(app, "current_frame", MagicMock())
        )
        app.set_windowed_size = MagicMock()
        app.show_sources_window = MagicMock()
        app.show_climate_page = MagicMock()
        app.season_wheel = MagicMock()
        app.security = MagicMock()
        app.question_pages = MagicMock()
        return app


if __name__ == "__main__":
    unittest.main()
