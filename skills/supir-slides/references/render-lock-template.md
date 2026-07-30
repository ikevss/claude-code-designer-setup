# Render Lock Reference

> Copy this structure into a project as `workNN/render_lock.md` and fill only real
> values. The lock is the canonical rendering constraint file.

## canvas

- format: slide169
- size: 1920x1080
- safe_margin: 72

## master

- layout_family: institutional_finance
- style_preset: institutional_research_default
- logo_policy: user_or_template_only
- footer_required: true
- source_note_required: research_or_user_requested
- visible_source_note_style: original_source_first_provider_fallback
- alpha_pai_visible_source_label: Alpha派_when_original_source_unavailable
- author_visibility: explicit_only
- hide_author_when_unknown: true
- audience_is_not_author_or_source: true
- forecast_assumption_note_required: when_relevant
- page_number_required: false
- no_page_number_unless_user_requested: true

## identity

- author_name: null
- author_confidence: unknown
- author_visible: false
- producer_name: null
- producer_confidence: unknown
- producer_visible: false
- audience_name: null
- audience_visible: false
- template_brand_role: retain_confirmed_template_brand_by_default
- source_provider_policy: original_source_first_then_provider
- alpha_pai_database_visible_source_policy: use_original_source_when_identifiable_else_normalize_to_Alpha派_keep_details_in_data_audit
- no_invented_department_names: true

## style

- rendering: institutional_research_report
- palette: generic_cool_blue_coral_lightblue
- primary: #01105C
- secondary_blue: #0C30A8
- accent: #2A66F6
- light_accent: #7DADFF
- critical_accent: #EF404A
- secondary: #5F6670
- pale_blue: #CFE4FF
- cover_background: #01105C
- cover_text: #FFFFFF
- inner_background_start: #EAF3FF
- inner_background_end: #FFFFFF
- neutral_surface: #F4F5F6
- grid: #D7E6FF
- positive: #C23531
- negative: #2E8B57
- text: #111827
- background: #FFFFFF
- evidence_panel: #FFFFFF
- default_reference_assets:
    - cover: assets/default-template/pptx-slide-01-cover.png
    - toc: assets/default-template/pptx-slide-02-contents.png
    - section: assets/default-template/pptx-slide-03-section.png
    - closing: assets/default-template/pptx-slide-04-title-page.png
    - title_page: assets/default-template/pptx-slide-04-title-page.png
    - content: assets/default-template/pptx-slide-04-title-page.png
    - diagram: assets/default-template/pptx-slide-04-title-page.png
    - evidence: assets/default-template/pptx-slide-04-title-page.png
- reference_asset_policy: use_role_specific_reference_image_for_image_generation_when_no_user_template
- reference_asset_text_policy: old_template_text_dates_sources_and_numbers_are_style_only_never_reuse_as_content
- reference_asset_brand_policy: alpha_paiwork_marks_are_builtin_template_brand_retain_by_default_remove_or_replace_when_user_requests
- typography: Source Han Sans SC / 思源黑体 plus Helvetica/Arial/Inter-like compact sans with tabular numerals; fall back to Noto Sans CJK SC or equivalent clear system CJK sans when Source Han Sans SC is unavailable
- typography_signature:
    - cover_title: Source Han Sans SC-like bold compact sans unless user/template specifies a distinctive display face
    - section_title: Source Han Sans SC-like bold compact sans unless user/template specifies a distinctive display face
    - page_title: Source Han Sans SC-like bold conclusion title, about 22-26pt depending on title length; long titles may be smaller
    - body: Source Han Sans SC-like compact readable sans, about 12.5-15pt
    - chart_axis_label: compact readable sans, about 11-13.5pt
    - table_cell: compact readable sans with tabular numerals, about 11-13.5pt
    - caption_source_note: smallest readable sans, about 8.5-10.5pt
    - avoid_substitution: if template titles are serif/Songti/Kaiti/calligraphic, do not replace with heavy bold sans
- typography_hierarchy:
    - cover_title: largest_consistent_title_scale
    - section_title: large_section_scale
    - page_title: consistent_conclusion_title_scale
    - subtitle: smaller_than_page_title
    - body: readable_main_text_scale
    - chart_axis_label: compact_but_readable
    - table_cell: compact_readable_with_tabular_numerals
    - caption_source_note: smallest_readable_scale
- typography_consistency_policy: same_role_same_size_across_deck
- min_body_text_size_policy: body_text_readable_at_presentation_size_source_notes_may_be_smaller
- max_body_text_size_policy: ordinary_content_body_should_not_be_oversized_or_title_like
- information_density_policy: ordinary_content_pages_must_not_trade_substance_for_oversized_type_icons_or_loose_spacing
- default_page_structure: top_claim_then_expression_mode
- cover_title_page_density_policy: no_kpi_strip_metric_row_core_viewpoint_or_evidence_summary_unless_user_explicitly_requests_metric_cover_or_reference_template_cover_uses_metric_summary_design
- global_content_expression_default: top_conclusion_then_viewpoint_evidence_or_visual_reasoning
- global_content_expression_priority: applies_unless_user_explicitly_requests_other_style
- ordinary_research_layout: upper_or_left_viewpoint_lower_or_right_evidence
- visual_reasoning_layout: top_conclusion_main_diagram_sparse_callouts
- slide_expression_modes: visual_reasoning_page/evidence_page/summary_page/appendix_data_page/transition_page
- target_main_deck_expression_mix: visual_reasoning_25_to_40_percent_evidence_25_to_40_percent_summary_10_to_20_percent
- visible_evidence_budget_main_deck: one_dominant_visual_argument_0_to_5_numbers_max_one_main_chart_or_two_compact_panels
- archive_evidence_policy: registry_and_excel_can_hold_full_proof_not_all_evidence_visible
- narrative_text_policy: 1_to_3_bold_leadin_paragraphs_or_2_to_4_substantive_bullets
- narrative_text_length: leadin_10_to_20_plus_body_50_to_150_cn_chars_per_paragraph_zone_max_350
- middle_viewpoint_role: primary_argument_carrier_not_decorative_copy
- do_not_compress_viewpoints_to_short_labels_unless_user_requests_minimal_style_or_page_role_requires_it: true
- sparse_content_page_treatment: reduce_font_icon_spacing_and_restore_causes_evidence_constraints_or_compact_artifact
- visible_conclusion_label_policy: direct_statement_no_meta_prefix
- title_terminal_punctuation_policy: no_trailing_full_stop_or_period_on_main_page_section_titles
- china_map_political_correctness_policy: Taiwan_is_part_of_China_Zangnan_is_part_of_China_no_McMahon_Line_as_China_boundary_Nansha_Islands_are_part_of_China_use_abstract_schematic_if_boundary_correctness_cannot_be_guaranteed
- narrative_zone_frame_policy: no_decorative_frame_unless_true_module_or_template
- header_zone: fixed_15_to_20_percent
- evidence_zone: bottom_45_to_60_percent
- frame_policy: open_grid_light_rules_no_default_rounded_cards
- icon_policy: ordinary_pages_0_to_1_icons_mechanism_pages_sparse_line_icons
- template_visual_override_policy: template_controls_visual_skin_page_roles_brand_and_typography_not_default_content_expression
- template_content_expression_override_requires: explicit_user_request_or_true_module_boundary
- table_style: flat_research_table_or_compact_three_line
- chart_style: flat_2d_excel_wind_broker_research
- cover_background_style: full_bleed_deep_indigo_with_white_type
- inner_background_style: subtle_pale_blue_to_white_gradient_report_canvas
- background_style: deep_blue_cover_and_subtle_pale_blue_gradient_content_pages
- ai_style_suppression: no_tech_launch_no_consulting_infographic_no_saas_dashboard_no_marketing_poster

## data_policy

- image_model_may_invent_numbers: false
- chart_table_text_source: deck_plan/data/registry only
- visible_evidence_source: visible_evidence_ids_only
- archive_evidence_not_rendered_by_default: true
- main_deck_claim_requires_argument_map: true
- main_deck_claim_requires_workpaper_registry: true
- page_evidence_registry_required_for_research_pages: true
- low_confidence_claim_treatment: scenario_monitoring_or_appendix
- deterministic_overlay_required_when: exact_value_table_or_over_10_exact_chart_labels_or_exact_text_over_350_cn_chars
- deterministic_overlay_required_for_tables: true
- text_fidelity_qa_required_for_pure_image_render: true
- unsupported_claim_marker: Needs-Source
- visible_source_note_original_source_first: true
- alpha_pai_platform_sources_visible_as: Alpha派_when_original_source_unavailable_or_platform_synthesized
- detailed_source_trail_location: workNN/data_audit.md
- machine_readable_source_trail_location: workNN/data/registry/
- recipient_or_audience_must_not_be_used_as_source: true

## compliance_policy

- audit_trail_required_for_all_external_data: true
- visible_source_note_required: research_or_user_requested
- visible_author_required: explicit_only
- unknown_author_treatment: omit_author_fields
- direct_trade_instruction_allowed: false
- investment_implication_style: scenario_monitoring_valuation_risk_reward
- generated_imagery_tone: emotionally_neutral

## page_rhythm

Page keys are internal only and must not be rendered as visible page numbers.

- P01: anchor
- P02: dense

## pages

- P01: cover
- P02: executive_summary_grid

## forbidden

- invented numbers
- fake source notes
- invented or fake logos not supplied by the user or confirmed as template brand assets
- forcing unconfirmed internal/default brand names from reference templates; confirmed template brand elements are retained by default unless the user requests removal or replacement
- unrequested page numbers, including page numbers carried over from a reference image
- China maps that omit Taiwan, exclude Zangnan/South Tibet, use the McMahon Line as China's boundary, or omit the Nansha Islands
- invented author / producer / research department
- using audience or recipient as source provider
- default rounded-card grids
- decorative rounded cards, shadow cards, glowing frames, gradient panels
- icon-per-bullet layouts
- oversized typography or icon rows that turn ordinary content pages into sparse slogan lists
- KPI strips, three-metric rows, large-number summaries, or evidence conclusion blocks on cover/title pages unless explicitly requested or clearly inherited from the selected reference template cover design
- dark neon technology backgrounds
- consulting infographic / SaaS dashboard / data-screen / marketing-poster look
- 3D charts, glowing charts, glassmorphism, glossy dashboard panels
- long visible source citations
- visible meta-label prefixes before conclusions or callouts
- unreadable small text
- promotional investment language
- emotionally manipulative market imagery
- changing pixels outside bbox for local edits

&nbsp;
