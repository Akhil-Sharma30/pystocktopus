"use strict";
(self.webpackChunkjupyterlab_plotly =
  self.webpackChunkjupyterlab_plotly || []).push([
  [855],
  {
    855: (e, t, a) => {
      a.r(t),
        a.d(t, {
          FigureModel: () => d,
          FigureView: () => y,
          MODULE_NAME: () => n.o,
          MODULE_VERSION: () => n.Y,
        });
      var s = a(900),
        l = a(431),
        i = a.n(l),
        r = a(478),
        o = a.n(r),
        n = a(657);
      window.PlotlyConfig = { MathJaxConfig: "local" };
      const _ = "^" + n.Y;
      class d extends s.DOMWidgetModel {
        defaults() {
          return Object.assign(Object.assign({}, super.defaults()), {
            _model_name: d.model_name,
            _model_module: d.model_module,
            _model_module_version: d.model_module_version,
            _view_name: d.view_name,
            _view_module: d.view_module,
            _view_module_version: d.view_module_version,
            _data: [],
            _layout: {},
            _config: {},
            _py2js_addTraces: null,
            _py2js_deleteTraces: null,
            _py2js_moveTraces: null,
            _py2js_restyle: null,
            _py2js_relayout: null,
            _py2js_update: null,
            _py2js_animate: null,
            _py2js_removeLayoutProps: null,
            _py2js_removeTraceProps: null,
            _js2py_restyle: null,
            _js2py_relayout: null,
            _js2py_update: null,
            _js2py_layoutDelta: null,
            _js2py_traceDeltas: null,
            _js2py_pointsCallback: null,
            _last_layout_edit_id: 0,
            _last_trace_edit_id: 0,
          });
        }
        initialize() {
          super.initialize.apply(this, arguments),
            this.on("change:_data", this.do_data, this),
            this.on("change:_layout", this.do_layout, this),
            this.on("change:_py2js_addTraces", this.do_addTraces, this),
            this.on("change:_py2js_deleteTraces", this.do_deleteTraces, this),
            this.on("change:_py2js_moveTraces", this.do_moveTraces, this),
            this.on("change:_py2js_restyle", this.do_restyle, this),
            this.on("change:_py2js_relayout", this.do_relayout, this),
            this.on("change:_py2js_update", this.do_update, this),
            this.on("change:_py2js_animate", this.do_animate, this),
            this.on(
              "change:_py2js_removeLayoutProps",
              this.do_removeLayoutProps,
              this,
            ),
            this.on(
              "change:_py2js_removeTraceProps",
              this.do_removeTraceProps,
              this,
            );
        }
        _normalize_trace_indexes(e) {
          if (null == e) {
            var t = this.get("_data").length;
            e = i().range(t);
          }
          return Array.isArray(e) || (e = [e]), e;
        }
        do_data() {}
        do_layout() {}
        do_addTraces() {
          var e = this.get("_py2js_addTraces");
          if (null !== e) {
            var t = this.get("_data"),
              a = e.trace_data;
            i().forEach(a, function (e) {
              t.push(e);
            });
          }
        }
        do_deleteTraces() {
          var e = this.get("_py2js_deleteTraces");
          if (null !== e) {
            var t = e.delete_inds,
              a = this.get("_data");
            t.slice()
              .reverse()
              .forEach(function (e) {
                a.splice(e, 1);
              });
          }
        }
        do_moveTraces() {
          var e = this.get("_py2js_moveTraces");
          null !== e &&
            (function (e, t, a) {
              for (var s = [], l = t.length - 1; l >= 0; l--)
                s.splice(0, 0, e[t[l]]), e.splice(t[l], 1);
              var r = i()(a).zip(s).sortBy(0).unzip().value();
              (a = r[0]), (s = r[1]);
              for (var o = 0; o < a.length; o++) e.splice(a[o], 0, s[o]);
            })(this.get("_data"), e.current_trace_inds, e.new_trace_inds);
        }
        do_restyle() {
          var e = this.get("_py2js_restyle");
          if (null !== e) {
            var t = e.restyle_data,
              a = this._normalize_trace_indexes(e.restyle_traces);
            f(this.get("_data"), t, a);
          }
        }
        do_relayout() {
          var e = this.get("_py2js_relayout");
          null !== e && v(this.get("_layout"), e.relayout_data);
        }
        do_update() {
          var e = this.get("_py2js_update");
          if (null !== e) {
            var t = e.style_data,
              a = e.layout_data,
              s = this._normalize_trace_indexes(e.style_traces);
            f(this.get("_data"), t, s), v(this.get("_layout"), a);
          }
        }
        do_animate() {
          var e = this.get("_py2js_animate");
          if (null !== e) {
            for (
              var t = e.style_data,
                a = e.layout_data,
                s = this._normalize_trace_indexes(e.style_traces),
                l = 0;
              l < t.length;
              l++
            ) {
              var i = t[l],
                r = s[l];
              v(this.get("_data")[r], i);
            }
            v(this.get("_layout"), a);
          }
        }
        do_removeLayoutProps() {
          var e = this.get("_py2js_removeLayoutProps");
          if (null !== e) {
            var t = e.remove_props;
            m(this.get("_layout"), t);
          }
        }
        do_removeTraceProps() {
          var e = this.get("_py2js_removeTraceProps");
          if (null !== e) {
            var t = e.remove_props,
              a = e.remove_trace;
            m(this.get("_data")[a], t);
          }
        }
      }
      (d.serializers = Object.assign(
        Object.assign({}, s.DOMWidgetModel.serializers),
        {
          _data: { deserialize: c, serialize: h },
          _layout: { deserialize: c, serialize: h },
          _py2js_addTraces: { deserialize: c, serialize: h },
          _py2js_deleteTraces: { deserialize: c, serialize: h },
          _py2js_moveTraces: { deserialize: c, serialize: h },
          _py2js_restyle: { deserialize: c, serialize: h },
          _py2js_relayout: { deserialize: c, serialize: h },
          _py2js_update: { deserialize: c, serialize: h },
          _py2js_animate: { deserialize: c, serialize: h },
          _py2js_removeLayoutProps: { deserialize: c, serialize: h },
          _py2js_removeTraceProps: { deserialize: c, serialize: h },
          _js2py_restyle: { deserialize: c, serialize: h },
          _js2py_relayout: { deserialize: c, serialize: h },
          _js2py_update: { deserialize: c, serialize: h },
          _js2py_layoutDelta: { deserialize: c, serialize: h },
          _js2py_traceDeltas: { deserialize: c, serialize: h },
          _js2py_pointsCallback: { deserialize: c, serialize: h },
        },
      )),
        (d.model_name = "FigureModel"),
        (d.model_module = n.o),
        (d.model_module_version = _),
        (d.view_name = "FigureView"),
        (d.view_module = n.o),
        (d.view_module_version = _);
      class y extends s.DOMWidgetView {
        perform_render() {
          var e,
            t,
            a,
            s,
            l = this;
          this.model.on("change:_py2js_addTraces", this.do_addTraces, this),
            this.model.on(
              "change:_py2js_deleteTraces",
              this.do_deleteTraces,
              this,
            ),
            this.model.on("change:_py2js_moveTraces", this.do_moveTraces, this),
            this.model.on("change:_py2js_restyle", this.do_restyle, this),
            this.model.on("change:_py2js_relayout", this.do_relayout, this),
            this.model.on("change:_py2js_update", this.do_update, this),
            this.model.on("change:_py2js_animate", this.do_animate, this),
            null ===
              (s =
                null ===
                  (a =
                    null ===
                      (t =
                        null === (e = window) || void 0 === e
                          ? void 0
                          : e.MathJax) || void 0 === t
                      ? void 0
                      : t.Hub) || void 0 === a
                  ? void 0
                  : a.Config) ||
              void 0 === s ||
              s.call(a, { SVG: { font: "STIX-Web" } });
          var r = this.model.get("_last_layout_edit_id"),
            n = this.model.get("_last_trace_edit_id");
          this.viewID = j();
          var _ = i().cloneDeep(this.model.get("_data")),
            d = i().cloneDeep(this.model.get("_layout"));
          d.height || (d.height = 360);
          var y = this.model.get("_config");
          (y.editSelection = !1),
            o()
              .newPlot(l.el, _, d, y)
              .then(function () {
                l._sendTraceDeltas(n),
                  l._sendLayoutDelta(r),
                  l.el.on("plotly_restyle", function (e) {
                    l.handle_plotly_restyle(e);
                  }),
                  l.el.on("plotly_relayout", function (e) {
                    l.handle_plotly_relayout(e);
                  }),
                  l.el.on("plotly_update", function (e) {
                    l.handle_plotly_update(e);
                  }),
                  l.el.on("plotly_click", function (e) {
                    l.handle_plotly_click(e);
                  }),
                  l.el.on("plotly_hover", function (e) {
                    l.handle_plotly_hover(e);
                  }),
                  l.el.on("plotly_unhover", function (e) {
                    l.handle_plotly_unhover(e);
                  }),
                  l.el.on("plotly_selected", function (e) {
                    l.handle_plotly_selected(e);
                  }),
                  l.el.on("plotly_deselect", function (e) {
                    l.handle_plotly_deselect(e);
                  }),
                  l.el.on("plotly_doubleclick", function (e) {
                    l.handle_plotly_doubleclick(e);
                  });
                var e = new CustomEvent("plotlywidget-after-render", {
                  detail: { element: l.el, viewID: l.viewID },
                });
                document.dispatchEvent(e);
              });
        }
        _processLuminoMessage(e, t) {
          switch ((t.apply(this, arguments), e.type)) {
            case "before-attach":
              var a = { showgrid: !1, showline: !1, tickvals: [] };
              o().newPlot(this.el, [], { xaxis: a, yaxis: a }),
                (this.resizeEventListener = () => {
                  this.autosizeFigure();
                }),
                window.addEventListener("resize", this.resizeEventListener);
              break;
            case "after-attach":
              this.perform_render();
              break;
            case "after-show":
            case "resize":
              this.autosizeFigure();
          }
        }
        processPhosphorMessage(e) {
          this._processLuminoMessage(e, super.processPhosphorMessage);
        }
        processLuminoMessage(e) {
          this._processLuminoMessage(e, super.processLuminoMessage);
        }
        autosizeFigure() {
          var e = this,
            t = e.model.get("_layout");
          (i().isNil(t) || i().isNil(t.width)) &&
            o()
              .Plots.resize(e.el)
              .then(function () {
                var t = e.model.get("_last_layout_edit_id");
                e._sendLayoutDelta(t);
              });
        }
        remove() {
          super.remove(),
            o().purge(this.el),
            window.removeEventListener("resize", this.resizeEventListener);
        }
        getFullData() {
          return i().mergeWith({}, this.el._fullData, this.el.data, p);
        }
        getFullLayout() {
          return i().mergeWith({}, this.el._fullLayout, this.el.layout, p);
        }
        buildPointsObject(e) {
          var t;
          if (e.hasOwnProperty("points")) {
            var a = e.points,
              s = a.length,
              l = !0;
            for (
              let e = 0;
              e < s && (l = l && a[e].hasOwnProperty("pointNumbers"));
              e++
            );
            var i = s;
            if (l) {
              i = 0;
              for (let e = 0; e < s; e++) i += a[e].pointNumbers.length;
            }
            if (
              ((t = {
                trace_indexes: new Array(i),
                point_indexes: new Array(i),
                xs: new Array(i),
                ys: new Array(i),
              }),
              l)
            ) {
              for (var r = 0, o = 0; o < s; o++)
                for (let e = 0; e < a[o].pointNumbers.length; e++, r++)
                  (t.point_indexes[r] = a[o].pointNumbers[e]),
                    (t.xs[r] = a[o].x),
                    (t.ys[r] = a[o].y),
                    (t.trace_indexes[r] = a[o].curveNumber);
              let e = !0;
              for (
                let a = 1;
                a < i &&
                ((e = e && t.trace_indexes[a - 1] === t.trace_indexes[a]), e);
                a++
              );
              e &&
                t.point_indexes.sort(function (e, t) {
                  return e - t;
                });
            } else
              for (o = 0; o < s; o++)
                (t.trace_indexes[o] = a[o].curveNumber),
                  (t.point_indexes[o] = a[o].pointNumber),
                  (t.xs[o] = a[o].x),
                  (t.ys[o] = a[o].y);
            if (void 0 !== a[0] && a[0].hasOwnProperty("z"))
              for (t.zs = new Array(s), o = 0; o < s; o++) t.zs[o] = a[o].z;
            return t;
          }
          return null;
        }
        buildInputDeviceStateObject(e) {
          var t = e.event;
          return void 0 === t
            ? null
            : {
                alt: t.altKey,
                ctrl: t.ctrlKey,
                meta: t.metaKey,
                shift: t.shiftKey,
                button: t.button,
                buttons: t.buttons,
              };
        }
        buildSelectorObject(e) {
          return e.hasOwnProperty("range")
            ? {
                type: "box",
                selector_state: { xrange: e.range.x, yrange: e.range.y },
              }
            : e.hasOwnProperty("lassoPoints")
            ? {
                type: "lasso",
                selector_state: { xs: e.lassoPoints.x, ys: e.lassoPoints.y },
              }
            : null;
        }
        handle_plotly_restyle(e) {
          if (
            !(null == e || (e[0] && e[0].hasOwnProperty("_doNotReportToPy")))
          ) {
            var t = {
              style_data: e[0],
              style_traces: e[1],
              source_view_id: this.viewID,
            };
            this.model.set("_js2py_restyle", t), this.touch();
          }
        }
        handle_plotly_relayout(e) {
          if (null != e && !e.hasOwnProperty("_doNotReportToPy")) {
            var t = { relayout_data: e, source_view_id: this.viewID };
            this.model.set("_js2py_relayout", t), this.touch();
          }
        }
        handle_plotly_update(e) {
          if (
            !(
              null == e ||
              (e.data && e.data[0].hasOwnProperty("_doNotReportToPy"))
            )
          ) {
            var t = {
              style_data: e.data[0],
              style_traces: e.data[1],
              layout_data: e.layout,
              source_view_id: this.viewID,
            };
            this.model.set("_js2py_update", t), this.touch();
          }
        }
        handle_plotly_click(e) {
          this._send_points_callback_message(e, "plotly_click");
        }
        handle_plotly_hover(e) {
          this._send_points_callback_message(e, "plotly_hover");
        }
        handle_plotly_unhover(e) {
          this._send_points_callback_message(e, "plotly_unhover");
        }
        handle_plotly_selected(e) {
          this._send_points_callback_message(e, "plotly_selected");
        }
        handle_plotly_deselect(e) {
          (e = { points: [] }),
            this._send_points_callback_message(e, "plotly_deselect");
        }
        _send_points_callback_message(e, t) {
          if (null != e) {
            var a = {
              event_type: t,
              points: this.buildPointsObject(e),
              device_state: this.buildInputDeviceStateObject(e),
              selector: this.buildSelectorObject(e),
            };
            null != a.points &&
              (this.model.set("_js2py_pointsCallback", a), this.touch());
          }
        }
        handle_plotly_doubleclick(e) {}
        do_addTraces() {
          var e = this.model.get("_py2js_addTraces");
          if (null !== e) {
            var t = this;
            o()
              .addTraces(this.el, e.trace_data)
              .then(function () {
                t._sendTraceDeltas(e.trace_edit_id);
                var a = e.layout_edit_id;
                t._sendLayoutDelta(a);
              });
          }
        }
        do_deleteTraces() {
          var e = this.model.get("_py2js_deleteTraces");
          if (null !== e) {
            var t = e.delete_inds,
              a = this;
            o()
              .deleteTraces(this.el, t)
              .then(function () {
                var t = e.trace_edit_id;
                a._sendTraceDeltas(t);
                var s = e.layout_edit_id;
                a._sendLayoutDelta(s);
              });
          }
        }
        do_moveTraces() {
          var e = this.model.get("_py2js_moveTraces");
          if (null !== e) {
            var t = e.current_trace_inds,
              a = e.new_trace_inds;
            i().isEqual(t, a) || o().moveTraces(this.el, t, a);
          }
        }
        do_restyle() {
          var e = this.model.get("_py2js_restyle");
          if (null !== e) {
            var t = e.restyle_data,
              a = this.model._normalize_trace_indexes(e.restyle_traces);
            (t._doNotReportToPy = !0),
              o().restyle(this.el, t, a),
              this._sendTraceDeltas(e.trace_edit_id);
            var s = e.layout_edit_id;
            this._sendLayoutDelta(s);
          }
        }
        do_relayout() {
          var e = this.model.get("_py2js_relayout");
          if (null !== e) {
            e.source_view_id !== this.viewID &&
              ((e.relayout_data._doNotReportToPy = !0),
              o().relayout(this.el, e.relayout_data));
            var t = e.layout_edit_id;
            this._sendLayoutDelta(t);
          }
        }
        do_update() {
          var e = this.model.get("_py2js_update");
          if (null !== e) {
            var t = e.style_data || {},
              a = e.layout_data || {},
              s = this.model._normalize_trace_indexes(e.style_traces);
            (t._doNotReportToPy = !0),
              o().update(this.el, t, a, s),
              this._sendTraceDeltas(e.trace_edit_id);
            var l = e.layout_edit_id;
            this._sendLayoutDelta(l);
          }
        }
        do_animate() {
          var e = this.model.get("_py2js_animate");
          if (null !== e) {
            var t = e.animation_opts,
              a = {
                data: e.style_data,
                layout: e.layout_data,
                traces: this.model._normalize_trace_indexes(e.style_traces),
                _doNotReportToPy: !0,
              },
              s = this;
            o()
              .animate(this.el, a, t)
              .then(function () {
                s._sendTraceDeltas(e.trace_edit_id);
                var t = e.layout_edit_id;
                s._sendLayoutDelta(t);
              });
          }
        }
        _sendLayoutDelta(e) {
          var t = {
            layout_delta: g(this.getFullLayout(), this.model.get("_layout")),
            layout_edit_id: e,
          };
          this.model.set("_js2py_layoutDelta", t), this.touch();
        }
        _sendTraceDeltas(e) {
          for (
            var t = this.model.get("_data"),
              a = i().range(t.length),
              s = new Array(a.length),
              l = this.getFullData(),
              r = 0;
            r < a.length;
            r++
          ) {
            var o = a[r];
            s[r] = g(l[o], t[o]);
          }
          var n = { trace_deltas: s, trace_edit_id: e };
          this.model.set("_js2py_traceDeltas", n), this.touch();
        }
      }
      const u = {
        int8: Int8Array,
        int16: Int16Array,
        int32: Int32Array,
        uint8: Uint8Array,
        uint16: Uint16Array,
        uint32: Uint32Array,
        float32: Float32Array,
        float64: Float64Array,
      };
      function h(e, t) {
        var a;
        if (i().isTypedArray(e))
          a = (function (e) {
            var t;
            if (e instanceof Int8Array) t = "int8";
            else if (e instanceof Int16Array) t = "int16";
            else if (e instanceof Int32Array) t = "int32";
            else if (e instanceof Uint8Array) t = "uint8";
            else if (e instanceof Uint16Array) t = "uint16";
            else if (e instanceof Uint32Array) t = "uint32";
            else if (e instanceof Float32Array) t = "float32";
            else {
              if (!(e instanceof Float64Array)) return e;
              t = "float64";
            }
            return { dtype: t, shape: [e.length], value: e.buffer };
          })(e);
        else if (Array.isArray(e)) {
          a = new Array(e.length);
          for (var s = 0; s < e.length; s++) a[s] = h(e[s]);
        } else if (i().isPlainObject(e))
          for (var l in ((a = {}), e)) e.hasOwnProperty(l) && (a[l] = h(e[l]));
        else a = void 0 === e ? "_undefined_" : e;
        return a;
      }
      function c(e, t) {
        var a;
        if (Array.isArray(e)) {
          a = new Array(e.length);
          for (var s = 0; s < e.length; s++) a[s] = c(e[s]);
        } else if (i().isPlainObject(e))
          if (
            (i().has(e, "value") || i().has(e, "buffer")) &&
            i().has(e, "dtype") &&
            i().has(e, "shape")
          )
            a = new (0, u[e.dtype])(
              i().has(e, "value") ? e.value.buffer : e.buffer.buffer,
            );
          else
            for (var l in ((a = {}), e))
              e.hasOwnProperty(l) && (a[l] = c(e[l]));
        else a = "_undefined_" === e ? void 0 : e;
        return a;
      }
      function p(e, t, a) {
        return "_" === a[0]
          ? null
          : ((s = t),
            !ArrayBuffer.isView(s) || s instanceof DataView ? void 0 : t);
        var s;
      }
      function v(e, t) {
        for (var a in t)
          if (t.hasOwnProperty(a)) {
            var s = t[a];
            null === s ? i().unset(e, a) : i().set(e, a, s);
          }
      }
      function f(e, t, a) {
        for (var s in t)
          if (t.hasOwnProperty(s)) {
            var l = t[s];
            Array.isArray(l) || (l = [l]);
            for (var r = 0; r < a.length; r++) {
              var o = e[a[r]],
                n = l[r % l.length];
              null === n ? i().unset(o, s) : void 0 !== n && i().set(o, s, n);
            }
          }
      }
      function m(e, t) {
        for (var a = 0; a < t.length; a++) {
          var s = t[a];
          i().unset(e, s);
        }
      }
      function g(e, t) {
        var a;
        for (var s in ((a = Array.isArray(e) ? new Array(e.length) : {}),
        null == t && (t = {}),
        e))
          if (
            "_" !== s[0] &&
            e.hasOwnProperty(s) &&
            null !== e[s] &&
            (!i().isEqual(e[s], t[s]) || "uid" === s)
          ) {
            var l = e[s];
            if (t.hasOwnProperty(s) && "object" == typeof l)
              if (Array.isArray(l))
                if (l.length > 0 && "object" == typeof l[0]) {
                  a[s] = new Array(l.length);
                  for (var r = 0; r < l.length; r++)
                    !Array.isArray(t[s]) || t[s].length <= r
                      ? (a[s][r] = l[r])
                      : (a[s][r] = g(l[r], t[s][r]));
                } else a[s] = l;
              else {
                var o = g(l, t[s]);
                Object.keys(o).length > 0 && (a[s] = o);
              }
            else
              "object" != typeof l || Array.isArray(l)
                ? void 0 !== l && "function" != typeof l && (a[s] = l)
                : (a[s] = g(l, {}));
          }
        return a;
      }
      function j(e, t, a, s) {
        if ((a || (a = 16), void 0 === t && (t = 24), t <= 0)) return "0";
        var l,
          i,
          r = Math.log(Math.pow(2, t)) / Math.log(a),
          o = "";
        for (l = 2; r === 1 / 0; l *= 2)
          r = (Math.log(Math.pow(2, t / l)) / Math.log(a)) * l;
        var n = r - Math.floor(r);
        for (l = 0; l < Math.floor(r); l++)
          o = Math.floor(Math.random() * a).toString(a) + o;
        n &&
          ((i = Math.pow(a, n)),
          (o = Math.floor(Math.random() * i).toString(a) + o));
        var _ = parseInt(o, a);
        return (e && e[o]) || (_ !== 1 / 0 && _ >= Math.pow(2, t))
          ? s > 10
            ? (console.warn("randstr failed uniqueness"), o)
            : j(e, t, a, (s || 0) + 1)
          : o;
      }
    },
  },
]);
