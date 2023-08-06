import {EditTool, EditToolView} from "@bokehjs/models/tools/edit/edit_tool"

import {Renderer} from "@bokehjs/models/renderers/renderer"
import {Label} from "@bokehjs/models/annotations/label"
import {PanEvent, MoveEvent, TapEvent} from "@bokehjs/core/ui_events"
import * as p from "@bokehjs/core/properties"
import {Color} from "@bokehjs/core/types"
import {values} from "@bokehjs/core/util/object"
import {bk_tool_icon_range} from "@bokehjs/styles/icons"

import {Annotation, AnnotationView} from "@bokehjs/models/annotations/annotation"
import * as mixins from "@bokehjs/core/property_mixins"
import {Line} from "@bokehjs/core/visuals"

export class LineMeasureView extends AnnotationView {
    model: LineMeasure
    visuals: LineMeasure.Visuals

    connect_signals(): void {
        super.connect_signals()
        this.connect(this.model.change, () => this.plot_view.request_paint(this))
    }

    _render(): void {
        if (!this.model.visible)
            return

        const {ctx} = this.layer
        ctx.save()

        ctx.beginPath()
        this.visuals.line.set_value(ctx)
        ctx.moveTo(this.model.x_start, this.model.y_start)
        ctx.lineTo(this.model.x_end, this.model.y_end)

        ctx.stroke()

        ctx.restore()
    }

    // render(): void {
    //     if (!this.model.visible)
    //         return
    //
    //     const {ctx} = this.layer
    //     ctx.save()
    //
    //     ctx.beginPath()
    //     this.visuals.line.set_value(ctx)
    //     ctx.moveTo(this.model.x_start, this.model.y_start)
    //     ctx.lineTo(this.model.x_end, this.model.y_end)
    //
    //     ctx.stroke()
    //
    //     ctx.restore()
    // }
}

export namespace LineMeasure {
    export type Attrs = p.AttrsOf<Props>

    export type Props = Annotation.Props & {
        x_start: p.Property<number>
        y_start: p.Property<number>
        x_end: p.Property<number>
        y_end: p.Property<number>
    } & Mixins

    export type Mixins = mixins.Line/*Scalar*/

    export type Visuals = Annotation.Visuals & { line: Line }
}

export interface LineMeasure extends LineMeasure.Attrs {
}

export class LineMeasure extends Annotation {
    properties: LineMeasure.Props
    __view_type__: LineMeasureView

    constructor(attrs?: Partial<LineMeasure.Attrs>) {
        super(attrs)
    }

    static init_LineMeasure(): void {
        this.prototype.default_view = LineMeasureView

        this.mixins<LineMeasure.Mixins>(mixins.Line/*Scalar*/)

        this.define<LineMeasure.Props>({
            x_start: [p.Number],
            x_end: [p.Number],
            y_start: [p.Number],
            y_end: [p.Number],
        })

        /*
        this.override({
          line_color: 'black',
        })
        */
    }
}

export class MeasureToolView extends EditToolView {
    model: MeasureTool

    connect_signals(): void {
        super.connect_signals()
        this.connect(this.model.properties.active.change, () => this._active_change())
    }

    _active_change(): void {
        if (!this.model.active)
            this._reset_measure_band()
    }

    _reset_measure_band(): void {
        this.model.measure_band.scale.x_start = 0
        this.model.measure_band.scale.y_start = 0

        this.model.measure_band.scale.x_end = 0
        this.model.measure_band.scale.y_end = 0

        this.model.measure_band.label.text = ""
        this.model.measure_band.pos_label.text = ""
    }

    /*
    _scroll(_ev: ScrollEvent): void {
        // const {delta} = _ev
        // if (delta != 0)
        this._reset_measure_band()
    }
     */

    _move(_ev: MoveEvent): void {
        const {sx, sy} = _ev
        const {frame} = this.plot_view

        // const x = frame.xscales.default.invert(sx)
        // const y = frame.yscales.default.invert(sy)

        const x = frame.x_scale.invert(sx)
        const y = frame.y_scale.invert(sy)

        this.model.measure_band.pos_label.text =
            "x=" + Number(x).toFixed(3) + " " + this.model.measure_unit +
            ", y=" + Number(y).toFixed(3) + " " + this.model.measure_unit

    }

    _move_exit(_e: MoveEvent): void {
        this.model.measure_band.pos_label.text = ""
    }

    _tap(_e: TapEvent): void {
        this._reset_measure_band()
    }

    _pan_start(_ev: PanEvent): void {
        const {sx, sy} = _ev

        this.model.measure_band.scale.x_start = sx
        this.model.measure_band.scale.y_start = sy
    }

    _pan(_ev: PanEvent): void {
        if (!this.model.active)
            return

        const {sx, sy} = _ev
        const {frame} = this.plot_view

        this.model.measure_band.scale.x_end = sx
        this.model.measure_band.scale.y_end = sy

        // const x_end = frame.xscales.default.invert(sx)
        // const y_end = frame.yscales.default.invert(sy)

        const x_end = frame.x_scale.invert(sx)
        const y_end = frame.y_scale.invert(sy)

        // const x_start = frame.xscales.default.invert(this.model.measure_band.scale.x_start)
        // const y_start = frame.yscales.default.invert(this.model.measure_band.scale.y_start)

        const x_start = frame.x_scale.invert(this.model.measure_band.scale.x_start)
        const y_start = frame.y_scale.invert(this.model.measure_band.scale.y_start)

        const dx = x_end - x_start
        const dy = y_end - y_start
        const distance = Math.sqrt(dx * dx + dy * dy)

        const angle_rad = Math.atan2(dy, dx)
        const angle = angle_rad * 180 / Math.PI

        this.model.measure_band.label.text =
            "distance=" + Number(distance).toFixed(3) + " " + this.model.measure_unit +
            ", angle= " + Number(angle).toFixed(2) + "° (" + Number(angle_rad).toFixed(2) + " rad)"
    }
}

export namespace MeasureTool {
    export type Attrs = p.AttrsOf<Props>

    export type Props = EditTool.Props & {
        measure_unit: p.Property<string>

        line_dash: p.Property<number[]>
        line_color: p.Property<Color>
        line_width: p.Property<number>
        line_alpha: p.Property<number>

        measure_band: p.Property<{ scale: LineMeasure, label: Label, pos_label: Label }>
    }
}

export interface MeasureTool extends MeasureTool.Attrs {
}

export class MeasureTool extends EditTool {
    properties: MeasureTool.Props
    __view_type__: MeasureToolView

    constructor(attrs?: Partial<MeasureTool.Attrs>) {
        super(attrs)
    }

    static init_MeasureTool(): void {
        this.prototype.default_view = MeasureToolView

        this.define<MeasureTool.Props>({
            measure_unit: [p.String, ''],
            line_dash: [p.Array, [4, 4]],
            line_color: [p.Color, 'black'],
            line_width: [p.Number, 1.5],
            line_alpha: [p.Number, 1],
        })

        this.internal({
            measure_band: [p.Any],
        })

        this.register_alias("measure", () => new MeasureTool())
    }

    tool_name = "Measure"
    icon = bk_tool_icon_range
    event_type = ["tap" as "tap", "pan" as "pan", "move" as "move", "scroll" as "scroll"]

    get synthetic_renderers(): Renderer[] {
        return values(this.measure_band)
    }

    initialize(): void {
        super.initialize()

        this.measure_band = {
            scale: new LineMeasure({
                x_start: 0,
                y_start: 0,
                x_end: 0,
                y_end: 0,
                line_dash: this.line_dash,
                line_color: this.line_color,
                line_width: this.line_width,
                line_alpha: this.line_alpha,
            }),
            label: new Label({
                x: 10,
                y: 35,
                x_units: "screen",
                y_units: "screen",
                text: "",
                text_font_size: "18px",
                background_fill_alpha: .75,
                background_fill_color: "white"
            }),
            pos_label: new Label({
                x: 10,
                y: 10,
                x_units: "screen",
                y_units: "screen",
                text: "",
                text_font_size: "18px",
                background_fill_alpha: .75,
                background_fill_color: "white"
            }),
        }
    }
}

