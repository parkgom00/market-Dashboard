(function () {
  "use strict";

  var D = window.DASH || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // 데이터 안의 글자가 화면 코드로 해석되지 않도록 안전 처리
  function esc(v) {
    return String(v == null ? "" : v).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function pad(n) { return n < 10 ? "0" + n : "" + n; }
  function ymd(y, m, d) { return y + "-" + pad(m + 1) + "-" + pad(d); }
  function pctText(v) {
    var n = Number(v) || 0;
    var cls = n > 0 ? "up" : n < 0 ? "down" : "flat";
    var sign = n > 0 ? "▲ +" : n < 0 ? "▼ " : "";
    return '<span class="' + cls + '">' + sign + n.toFixed(2) + "%</span>";
  }
  function bpText(v) {
    var n = Number(v) || 0;
    var cls = n > 0 ? "up" : n < 0 ? "down" : "flat";
    return '<span class="' + cls + '">' + (n > 0 ? "▲ +" : n < 0 ? "▼ " : "") + n.toFixed(1) + "bp</span>";
  }
  function num(v) { return Number(v || 0).toLocaleString("ko-KR"); }
  function sampleNote(o) {
    return o && o.sample ? '<div class="banner" style="margin:0 0 10px">이 탭은 아직 샘플 데이터입니다. 실제 시세·분석이 아닙니다.</div>' : "";
  }
  function safeUrl(u) { return /^https?:\/\//i.test(u || "") ? u : "#"; }

  /* ---------- 공통: 선택 버튼(세그먼트) ---------- */
  function seg(items, current, attr) {
    return '<div class="seg">' + items.map(function (it) {
      return '<button type="button" ' + attr + '="' + esc(it.id) + '" class="' + (it.id === current ? "on" : "") + '">' + esc(it.label) + "</button>";
    }).join("") + "</div>";
  }

  /* ---------- 1장: 캘린더 ---------- */
  var TYPE = {
    holiday: "휴장", econ: "경제지표", earnings: "실적", event: "이벤트"
  };

  function renderCalendar() {
    var root = $("#tab-calendar");
    var events = (D.calendar && D.calendar.events) || [];
    var now = new Date();
    var year = now.getFullYear(), month = now.getMonth();
    var selected = ymd(now.getFullYear(), now.getMonth(), now.getDate());
    var todayStr = selected;

    function eventsOn(date) { return events.filter(function (e) { return e.date === date; }); }

    function draw() {
      var first = new Date(year, month, 1).getDay();
      var days = new Date(year, month + 1, 0).getDate();
      var h = '<div class="cal-head"><button type="button" data-nav="-1" aria-label="이전 달">‹</button>' +
        "<strong>" + year + "년 " + (month + 1) + "월</strong>" +
        '<button type="button" data-nav="1" aria-label="다음 달">›</button></div>';

      h += '<div class="cal-grid">';
      ["일", "월", "화", "수", "목", "금", "토"].forEach(function (w, i) {
        h += '<div class="cal-dow ' + (i === 0 ? "sun" : i === 6 ? "sat" : "") + '">' + w + "</div>";
      });
      for (var b = 0; b < first; b++) h += '<div class="cal-day blank"></div>';
      for (var d = 1; d <= days; d++) {
        var ds = ymd(year, month, d);
        var dow = (first + d - 1) % 7;
        var evs = eventsOn(ds);
        var dots = evs.slice(0, 4).map(function (e) { return '<i class="dot ' + esc(e.type) + '"></i>'; }).join("");
        h += '<button type="button" data-date="' + ds + '" class="cal-day ' +
          (dow === 0 ? "sun " : dow === 6 ? "sat " : "") +
          (ds === todayStr ? "today " : "") + (ds === selected ? "sel" : "") + '">' +
          '<span class="n">' + d + '</span><span class="dots">' + dots + "</span></button>";
      }
      h += "</div>";

      h += '<div class="legend">' + Object.keys(TYPE).map(function (k) {
        return '<span><i class="dot ' + k + '"></i>' + TYPE[k] + "</span>";
      }).join("") + "</div>";

      var selEvs = eventsOn(selected);
      h += '<div class="card"><h3>' + esc(selected) + " 일정</h3>";
      h += selEvs.length ? selEvs.map(evRow).join("") : '<div class="muted">등록된 일정이 없습니다.</div>';
      h += "</div>";

      var prefix = year + "-" + pad(month + 1);
      var monthEvs = events.filter(function (e) { return e.date.indexOf(prefix) === 0; })
        .sort(function (a, b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : 0; });
      h += '<div class="card"><h3>이달의 주요 일정</h3>';
      h += monthEvs.length ? monthEvs.map(function (e) { return evRow(e, true); }).join("") : '<div class="muted">이 달에 등록된 일정이 없습니다.</div>';
      h += "</div>";

      root.innerHTML = '<h2>마켓 캘린더</h2>' + h;
    }

    function evRow(e, withDate) {
      return '<div class="ev">' +
        (withDate ? '<span class="d">' + esc(e.date.slice(5).replace("-", "/")) + "</span>" : "") +
        '<span class="tag ' + esc(e.type) + '">' + esc(TYPE[e.type] || e.type) + "</span>" +
        "<span>" + (e.market ? '<span class="muted">' + esc(e.market) + " · </span>" : "") + (e.time ? '<span class="muted">' + esc(e.time) + " </span>" : "") + (e.major ? "<b>" + esc(e.title) + "</b>" : esc(e.title)) +
        ((e.result || []).length ? '<div class="evres">' + e.result.map(function (r) { return "<div>" + esc(r) + "</div>"; }).join("") + "</div>" : "") +
        "</span></div>";
    }

    root.addEventListener("click", function (ev) {
      var nav = ev.target.closest("[data-nav]");
      var day = ev.target.closest("[data-date]");
      if (nav) {
        month += Number(nav.getAttribute("data-nav"));
        if (month < 0) { month = 11; year--; }
        if (month > 11) { month = 0; year++; }
        selected = ymd(year, month, 1);
        draw();
      } else if (day) {
        selected = day.getAttribute("data-date");
        draw();
      }
    });
    draw();
  }

  /* ---------- 히트맵 공통 ---------- */
  var HEAT_MAX = 3;   // ±3% 에서 가장 진한 색
  function heatColor(pct, max) {
    var p = Number(pct) || 0, t = Math.min(Math.abs(p) / (max || HEAT_MAX), 1);
    var n = [72, 78, 92], to = p >= 0 ? [220, 38, 44] : [26, 90, 214];
    t = Math.pow(t, 0.75);
    return "rgb(" + n.map(function (v, i) { return Math.round(v + (to[i] - v) * t); }).join(",") + ")";
  }
  function heatLegend() {
    return '<div class="hm-legend">' + [-3, -2, -1, 0, 1, 2, 3].map(function (v) {
      return '<span style="background:' + heatColor(v) + '">' + (v > 0 ? "+" : "") + v + "%</span>";
    }).join("") + "</div>";
  }
  /* 네모 나누기(스퀘어리파이): nodes[{v}] 를 x,y,w,h 안에 값 비율대로 채운다 */
  function squarify(nodes, x, y, w, h) {
    var total = nodes.reduce(function (s, n) { return s + n.v; }, 0), out = [];
    if (total <= 0 || w <= 0 || h <= 0) return out;
    var items = nodes.map(function (n) { return { n: n, a: n.v / total * w * h }; }).sort(function (p, q) { return q.a - p.a; });
    var i = 0;
    while (i < items.length) {
      var shortSide = Math.min(w, h), row = [], area = 0, best = Infinity, mx = 0, mn = Infinity;
      while (i < items.length) {
        var a = items[i].a, na = area + a, nmx = Math.max(mx, a), nmn = Math.min(mn, a);
        var worst = Math.max(shortSide * shortSide * nmx / (na * na), na * na / (shortSide * shortSide * nmn));
        if (row.length && worst > best) break;
        row.push(items[i]); area = na; best = worst; mx = nmx; mn = nmn; i++;
      }
      var thick = area / shortSide, off = 0;
      row.forEach(function (r) {
        var len = r.a / thick;
        if (w >= h) out.push({ n: r.n, x: x, y: y + off, w: thick, h: len });
        else out.push({ n: r.n, x: x + off, y: y, w: len, h: thick });
        off += len;
      });
      if (w >= h) { x += thick; w -= thick; } else { y += thick; h -= thick; }
    }
    return out;
  }
  var HM_W = 100, HM_H = 150;   // 가상 좌표 (가로 100 = 화면 폭)
  function heatmapHtml(items) {
    var secs = [];
    items.forEach(function (it, idx) {
      var g = secs.filter(function (x) { return x.name === it.s; })[0];
      if (!g) { g = { name: it.s, v: 0, kids: [] }; secs.push(g); }
      g.v += it.c; g.kids.push({ v: it.c, it: it, idx: idx });
    });
    var pos = function (r) {
      return "left:" + (r.x / HM_W * 100).toFixed(3) + "%;top:" + (r.y / HM_H * 100).toFixed(3) + "%;width:" + (r.w / HM_W * 100).toFixed(3) + "%;height:" + (r.h / HM_H * 100).toFixed(3) + "%;";
    };
    var fs = function (u) { return "font-size:" + (u * 3.6).toFixed(1) + "px;font-size:" + u.toFixed(2) + "cqw;"; };
    var h = "";
    squarify(secs, 0, 0, HM_W, HM_H).forEach(function (sr) {
      var hd = sr.h > 9 && sr.w > 12 ? 3.6 : 0;
      h += '<div class="hm-sec" style="' + pos(sr) + '">' + (hd ? '<div class="hm-sechd" style="' + fs(2.5) + "height:" + (hd / sr.h * 100).toFixed(2) + '%">' + esc(sr.n.name) + "</div>" : "") + "</div>";
      squarify(sr.n.kids, sr.x, sr.y + hd, sr.w, sr.h - hd).forEach(function (r) {
        var it = r.n.it, len = it.t.length;
        var f = Math.min(r.w / (len * 0.66 + 0.5), r.h * 0.4, 6);
        var label = "";
        if (f >= 1.7) {
          label = '<b style="' + fs(f) + '">' + esc(it.t) + "</b>";
          var pf = Math.max(Math.min(f * 0.72, r.w / 4.2), 1.6);
          if (r.h > f * 1.25 + pf * 1.3 && r.w > pf * 3.6) label += '<span style="' + fs(pf) + '">' + (it.p > 0 ? "+" : "") + it.p.toFixed(2) + "%</span>";
        }
        h += '<div class="hm-cell" data-hm="' + r.n.idx + '" style="' + pos(r) + "background:" + heatColor(it.p) + '">' + label + "</div>";
      });
    });
    return h;
  }
  function capText(b) { return b >= 1000 ? "$" + (b / 1000).toFixed(2) + "T" : "$" + Math.round(b) + "B"; }

  /* ---------- 2장: 미국장 ---------- */
  function renderUS() {
    var root = $("#tab-us");
    var u = D.usmarket || {};
    var br = u.brief || null;
    var h = sampleNote(u) + "<h2>미국장 마감 &amp; 국장 대응</h2>";
    h += '<div class="muted" style="margin:-6px 0 10px">' + esc(u.asOf || "") + (u.staleNote ? " · " + esc(u.staleNote) : "") + "</div>";

    // 1) 지수·금리·환율·원자재
    var groups = [];
    (u.indices || []).forEach(function (i) {
      var g = groups.filter(function (x) { return x.name === (i.group || "지수"); })[0];
      if (!g) { g = { name: i.group || "지수", items: [] }; groups.push(g); }
      g.items.push(i);
    });
    groups.forEach(function (g) {
      h += '<div class="sub-title">' + esc(g.name) + '</div><div class="idx">' + g.items.map(function (i) {
        var chg = i.changeBp != null ? '<div class="pc">' + bpText(i.changeBp) + "</div>" : '<div class="pc">' + pctText(i.changePct) + "</div>";
        return '<div class="card"><div class="nm">' + esc(i.name) + "</div>" + chg + (i.close ? '<div class="nm">' + num(i.close) + (i.kind === "yield" ? "%" : "") + "</div>" : "") + "</div>";
      }).join("") + "</div>";
    });

    // 1-2) 간밤 미국장 요약·시황 (한국경제TV #당잠사 영상을 AI 가 요약)
    var dj = D.dangjamsa || {};
    var bold = function (t) { return esc(t).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>"); };
    if ((dj.parts || []).length) {
      h += '<div class="card djcard"><div class="row"><h3>간밤 미국장 요약 · 시황</h3><span class="meta">' + esc((dj.forDate || "").slice(5).replace("-", "/")) + " 방송</span></div>" +
        (dj.headline ? '<p class="djhead">' + bold(dj.headline) + "</p>" : "") +
        dj.parts.map(function (p, i) {
          return '<details class="djpart"' + (i < 2 ? " open" : "") + "><summary>" + (i + 1) + ". " + esc(p.title || "요점") + "</summary><ul>" +
            (p.points || []).map(function (x) { return "<li>" + bold(x) + "</li>"; }).join("") + "</ul></details>";
        }).join("") +
        '<div class="muted">한국경제TV 유튜브 <a href="' + safeUrl(dj.sumUrl || dj.url) + '" target="_blank" rel="noopener noreferrer">#당잠사 방송</a>을 AI(제미나이)가 요약한 내용입니다' +
        (dj.generatedAt ? " · " + esc(dj.generatedAt) + " 정리" : "") + ". 방송 내용 요약이며 투자 권유가 아닙니다." +
        (dj.status ? "<br>" + esc(dj.status) : "") + "</div></div>";
    } else {
      h += '<div class="card djcard"><h3>간밤 미국장 요약 · 시황</h3><div class="muted">한국경제TV #당잠사 방송을 매일 아침 AI가 요약해 여기에 보여줍니다. ' +
        (dj.status ? esc(dj.status) : "아직 요약이 만들어지지 않았습니다.") +
        (dj.url ? ' <a href="' + safeUrl(dj.url) + '" target="_blank" rel="noopener noreferrer">오늘 방송 보기 ›</a>' : "") + "</div></div>";
    }

    // 2) 히트맵 (S&P 500 시총 상위: 네모 크기 = 시가총액, 색 = 등락률)
    var hm = u.heatmap && (u.heatmap.items || []).length ? u.heatmap : null;
    if (hm) {
      h += '<div class="card"><h3>미국 히트맵</h3><div class="muted">' + esc(hm.source || "") + " · " + hm.items.length + "종목 · " + esc(u.asOf || "") + "</div>" +
        '<div class="hm-wrap"><div class="hm" id="us-hm">' + heatmapHtml(hm.items) + "</div></div>" +
        heatLegend() +
        '<div class="hm-info" id="us-hm-info">네모를 누르면 종목 정보가 보입니다. 크기는 시가총액, 색은 전일 대비 등락률입니다.</div></div>';
    } else if (u.heatmapStatus) {
      h += '<div class="card"><h3>미국 히트맵</h3><div class="muted">' + esc(u.heatmapStatus) + "</div></div>";
    }

    // 3) 업종별 성과 (대표 ETF 등락률, 색 진하기 = 강약)
    var sec = u.sectors || [];
    if (sec.length) {
      var sorted = sec.slice().sort(function (x, y) { return y.changePct - x.changePct; });
      var names = function (arr) { return arr.map(function (x) { return esc(x.name) + " " + (x.changePct > 0 ? "+" : "") + x.changePct.toFixed(2) + "%"; }).join(" · "); };
      var gs = [];
      sec.forEach(function (x) {
        var g = gs.filter(function (y) { return y.name === x.group; })[0];
        if (!g) { g = { name: x.group, items: [] }; gs.push(g); }
        g.items.push(x);
      });
      h += '<div class="card"><h3>업종별 성과</h3>' +
        '<div class="secsum"><span class="up">강</span> ' + names(sorted.slice(0, 3)) + '<br><span class="down">약</span> ' + names(sorted.slice(-3).reverse()) + "</div>" +
        gs.map(function (g) {
          return '<div class="sub-title">' + esc(g.name) + '</div><div class="secgrid">' +
            g.items.slice().sort(function (x, y) { return y.changePct - x.changePct; }).map(function (x) {
              return '<div class="sectile" style="background:' + heatColor(x.changePct) + '" title="' + esc(x.symbol) + '">' +
                '<div class="sn">' + esc(x.name) + '</div><div class="sp">' + (x.changePct > 0 ? "+" : "") + x.changePct.toFixed(2) + "%</div>" +
                (x.kr ? '<div class="sk">' + esc(x.kr) + "</div>" : "") + "</div>";
            }).join("") + "</div>";
        }).join("") + heatLegend() + '<div class="muted">업종 대표 ETF의 전일 대비 등락률입니다. 작은 글씨는 연결되는 국내 업종입니다.</div></div>';
    }

    // 4) AI 브리핑 (있을 때만)
    if (br) {
      h += '<div class="card"><h3>간밤 미국장 이슈</h3><p class="para">' + esc(br.usMarket) + "</p>" +
        (br.sectorFlow ? '<div class="sub-title">업종 흐름</div><p class="para">' + esc(br.sectorFlow) + "</p>" : "") +
        (br.koreaImpact ? '<div class="sub-title">오늘 국장에 미칠 영향</div><p class="para">' + esc(br.koreaImpact) + "</p>" : "") +
        '<div class="muted">' + (br.grounded ? "AI가 구글 검색 근거로 정리한 내용입니다." : "검색 근거 없이 시세만 보고 해석한 내용입니다(원인은 확인되지 않았을 수 있음).") +
        " 참고용이며 투자 권유가 아닙니다.</div></div>";
      if ((br.news || []).length) {
        h += '<div class="card"><h3>주요 뉴스와 국내 파급</h3>' + br.news.map(function (n) {
          return '<div class="stock"><div class="nm">' + esc(n.title) + "</div><div>" + esc(n.fact) + "</div>" +
            (n.korea_impact ? '<div class="muted">국내 파급: ' + esc(n.korea_impact) + "</div>" : "") + "</div>";
        }).join("") + "</div>";
      }
      var chk = function (title, arr, cls) {
        if (!(arr || []).length) return "";
        return '<div class="card"><h3>' + title + "</h3>" + arr.map(function (c) {
          return '<div class="stock ' + cls + '"><div class="nm">' + esc(c.theme) + (c.us ? ' <span class="meta">' + esc(c.us) + "</span>" : "") + "</div>" +
            (c.cause ? "<div>" + esc(c.cause) + "</div>" : "") + (c.action ? '<div class="muted">점검 포인트: ' + esc(c.action) + "</div>" : "") + "</div>";
        }).join("") + "</div>";
      };
      h += chk("오늘 국장 체크 · 조심할 점", br.caution, "caution") + chk("오늘 국장 체크 · 눈여겨볼 곳", br.watch, "watch");
    } else if ((u.summary || []).length) {
      h += '<div class="card"><h3>어제 미국장 이슈</h3><ul class="plain">' + u.summary.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul></div>";
    }

    // 5) 미국 주도 테마 → 국내 관련주
    var STR = ["", "●○○ 테마 동조", "●●○ 같은 업황", "●●● 직접 연관"];
    var krPick = function (p, reason) {
      var q = ((D.quotes || {}).kr || {})[p.code];
      var nm = p.code ? '<a href="https://m.stock.naver.com/domestic/stock/' + encodeURIComponent(p.code) + '/total" target="_blank" rel="noopener noreferrer">' + esc(p.name) + "</a>" : esc(p.name);
      return '<div class="krpick"><div class="row"><div><span class="nm">' + nm + "</span>" +
        (p.strength ? ' <span class="str s' + p.strength + '">' + STR[p.strength] + "</span>" : "") + "</div>" +
        (q ? '<span class="krq">' + num(q.price) + " " + pctText(q.pct) + "</span>" : "") + "</div>" +
        (reason ? '<div class="meta">' + esc(reason) + "</div>" : "") + "</div>";
    };
    var themeCard = function (t, i, weak) {
      var c = '<div class="card tcard' + (weak ? " weak" : "") + '"><div class="row"><h3>' + (weak ? "🧊 " : '<span class="rank">' + (i + 1) + "</span> ") + esc(t.name) + "</h3>" +
        '<b class="' + (t.changePct > 0 ? "up" : t.changePct < 0 ? "down" : "flat") + ' tpct">' + (t.changePct > 0 ? "▲ +" : t.changePct < 0 ? "▼ " : "") + t.changePct.toFixed(2) + "%</b></div>" +
        '<div class="sub-title">🇺🇸 미국 ' + (weak ? "약세 종목" : "주도주") + '</div><div class="uschips">' + (t.usStocks || []).map(function (x) {
          return '<span class="uschip" style="background:' + heatColor(x.changePct) + '"><b>' + esc(x.name) + "</b> " + esc(x.ticker) + " " + (x.changePct > 0 ? "+" : "") + x.changePct.toFixed(2) + "%</span>";
        }).join("") + "</div>";
      if (t.logic) c += '<div class="linkbox"><span class="lk">🔗 연결 로직</span>' + esc(t.logic) + "</div>";
      if ((t.krStocks || []).length) {
        c += '<div class="sub-title">🇰🇷 국내 관련주</div>' + t.krStocks.map(function (p) { return krPick(p, p.link); }).join("");
      }
      return c + "</div>";
    };
    if ((u.themes || []).length) {
      h += "<h2>미국 주도 테마 → 국내 관련주</h2>";
      h += u.themes.map(function (t, i) { return themeCard(t, i, false); }).join("");
      if ((u.weakThemes || []).length) {
        h += '<details class="weakbox"><summary>약했던 테마 ' + u.weakThemes.length + "개 보기</summary>" +
          u.weakThemes.map(function (t, i) { return themeCard(t, i, true); }).join("") + "</details>";
      }
      h += '<div class="muted" style="margin:6px 0 14px">테마 등락률은 미국 대표 종목의 평균입니다. 연결 로직과 국내 관련주는 미리 정리해 둔 일반적인 산업 연결이며 그날의 뉴스를 반영한 추천이 아닙니다. 국내 종목 옆 숫자는 오늘 현재가입니다.</div>';
    }

    // 5-2) 서학개미 TOP 50 (예탁결제원 세이브로)
    var sh = u.seohak;
    if (sh && ((sh.hold || []).length || (sh.netbuy || []).length)) {
      var usd = function (v) {
        var n = Number(v) || 0, a = Math.abs(n);
        return (n < 0 ? "-" : "") + (a >= 1e8 ? (a / 1e8).toFixed(1) + "억 달러" : num(Math.round(a / 1e4)) + "만 달러");
      };
      var shRow = function (x) {
        return '<div class="shrow"><span class="shrank">' + x.rank + '</span><div class="shname"><span class="nm">' + esc(x.name) + "</span>" +
          (x.name.indexOf("(" + x.ticker + ")") < 0 ? ' <span class="meta">' + esc(x.ticker) + "</span>" : "") +
          (x.etf ? ' <span class="chip etf">ETF</span>' : "") + '<div class="meta">' + usd(x.usd) + "</div></div>" +
          '<div class="shpct">' + (x.changePct != null ? pctText(x.changePct) : '<span class="meta">-</span>') + "</div></div>";
      };
      var shList = function (rows) {
        return rows.slice(0, 10).map(shRow).join("") +
          (rows.length > 10 ? '<details class="weakbox"><summary>11~' + rows.length + "위 보기</summary>" + rows.slice(10).map(shRow).join("") + "</details>" : "");
      };
      h += "<h2>서학개미 TOP 50</h2>" + '<div class="card" id="us-seohak">' +
        '<div class="seg"><button type="button" data-sh="hold" class="on">보관금액 상위</button><button type="button" data-sh="net">최근 1주 순매수</button></div>' +
        '<div data-shp="hold"><div class="muted">국내 투자자가 가장 많이 보유한 미국 종목 · 기준일 ' + esc(sh.holdAsOf || "-") + "</div>" + shList(sh.hold || []) + "</div>" +
        '<div data-shp="net" hidden><div class="muted">국내 투자자가 가장 많이 순매수한 미국 종목 · ' + esc(sh.netPeriod || "-") + " 결제 기준</div>" + shList(sh.netbuy || []) + "</div>" +
        '<div class="muted" style="margin-top:6px">출처: 한국예탁결제원 세이브로(외화증권 종목별 내역). 오른쪽 숫자는 직전 미국장 등락률입니다. ETF를 뺀 종목은 중장기 스캔 대상에 자동으로 포함됩니다.</div></div>';
    }

    // 6) AI가 그날 뉴스로 찾은 연결 (브리핑이 만들어진 날만)
    if (br && (br.connections || []).length) {
      h += "<h2>AI가 찾은 오늘의 연결</h2>";
      br.connections.forEach(function (c) {
        h += '<div class="card tcard"><div class="conn-sector"><b>' + esc(c.sector) + "</b>" +
          (c.sectorChange != null ? ' <span class="meta">업종</span> ' + pctText(c.sectorChange) : "") + "</div>" +
          '<div class="row"><div><span class="nm">' + esc(c.usName) + '</span> <span class="meta">' + esc(c.usTicker) + "</span></div>" +
          (c.usChange != null ? pctText(c.usChange) : '<span class="meta">' + (c.direction === "down" ? "약세" : "강세") + "</span>") + "</div>" +
          (c.cause ? '<div class="para">' + esc(c.cause) + "</div>" : "") +
          (c.logic ? '<div class="linkbox"><span class="lk">🔗 연결 로직</span>' + esc(c.logic) + "</div>" : "") +
          '<div class="sub-title">🇰🇷 국내 관련주</div>' +
          (c.koreaPicks || []).map(function (p) { return krPick(p, p.reason); }).join("") + "</div>";
      });
      h += '<div class="muted">AI가 검색으로 추정한 연결이라 실제 투자 전 확인이 필요합니다.</div>';
    }
    if (!br && u.briefStatus) {
      h += '<details class="weakbox"><summary>AI 브리핑은 아직 만들어지지 않았습니다</summary><div class="muted">' + esc(u.briefStatus) + "</div></details>";
    }
    if (!(u.indices || []).length) h += '<div class="card empty">아직 수집된 데이터가 없습니다.</div>';
    root.innerHTML = h;
    root.onclick = function (ev) {
      var sb = ev.target.closest("[data-sh]");
      if (sb) {
        var which = sb.getAttribute("data-sh");
        $$("#us-seohak [data-sh]").forEach(function (x) { x.classList.toggle("on", x === sb); });
        $$("#us-seohak [data-shp]").forEach(function (x) { x.hidden = x.getAttribute("data-shp") !== which; });
        return;
      }
      var c = ev.target.closest("[data-hm]");
      if (!c || !hm) return;
      var it = hm.items[Number(c.getAttribute("data-hm"))];
      $$("#us-hm .hm-cell.on").forEach(function (x) { x.classList.remove("on"); });
      c.classList.add("on");
      $("#us-hm-info").innerHTML = '<b>' + esc(it.t) + "</b> " + esc(it.n) + ' <span class="meta">' + esc(it.s) + "</span> " + pctText(it.p) +
        ' <span class="meta">시총 ' + capText(it.c) + '</span> <a href="https://finance.yahoo.com/chart/' + encodeURIComponent(it.t.replace(".", "-")) + '" target="_blank" rel="noopener noreferrer">📈 차트</a>';
    };
  }

  /* ---------- 특징주(실시간) ---------- */
  var LIVE_STRONG = 3;   // +3% 이상이면 '강한 종목'(빨강)
  var LIVE_WEAK = -3;    // -3% 이하이면 '약한 종목'(초록)
  var liveMarket = "kr";
  var liveStatus = "";   // 새로고침 결과 문구
  var liveBusy = false;

  function strengthClass(v) {
    var n = Number(v) || 0;
    return n >= LIVE_STRONG ? "strong" : n <= LIVE_WEAK ? "weak" : "";
  }
  function rankList(items, extra) {
    if (!items || !items.length) return '<div class="muted">데이터가 없습니다.</div>';
    return items.map(function (s, i) {
      return '<div class="rank"><div class="no">' + (i + 1) + '</div><div class="mid"><div class="nm">' + esc(s.name) + '</div>' +
        '<div class="meta">' + esc(s.code) + (s.price != null ? " · " + num(s.price) : "") + "</div></div>" +
        '<div class="rt">' + pctText(s.changePct) + (extra ? '<div class="meta">' + extra(s) + "</div>" : "") + "</div></div>";
    }).join("");
  }

  var RANK_SHOW = 10;      // 처음에는 10위까지, '더보기'를 누르면 20위까지
  var liveMore = {};
  function rankBlock(key, items, extra) {
    if (!items || !items.length) return rankList(items);
    var open = !!liveMore[key + liveMarket];
    var shown = open ? items : items.slice(0, RANK_SHOW);
    var html = rankList(shown, extra);
    if (items.length > RANK_SHOW) {
      html += '<button type="button" class="morebtn" data-more="' + key + '">' + (open ? "접기 ▲" : (RANK_SHOW + 1) + "~" + items.length + "위 더보기 ▼") + "</button>";
    }
    return html;
  }

  /* ---------- 테마 순환매 (특징주 탭 안) ---------- */
  var rotPeriod = "1";
  function rotationHtml() {
    var R = D.rotation;
    if (!R || !(R.days || []).length) return '<div class="card empty">아직 순환매 자료가 없습니다. 장 마감 후(16:30 무렵) 만들어집니다.</div>';
    var md = function (d) { return d.slice(5).replace("-", "/"); };
    var sgn = function (v) { return (v > 0 ? "+" : "") + Number(v).toFixed(2) + "%"; };
    var h = '<div class="muted" style="margin:-2px 0 8px">기준일 ' + esc(R.asOf || "") + " · 네이버 테마 " + (R.themeCount || 0) + "개 · 장 마감 후 하루 한 번 갱신</div>";

    // 1) 돈이 들어온 테마
    var list = (R.inflow || {})[rotPeriod] || [];
    h += '<div class="card"><h3>돈이 들어온 테마</h3>' +
      seg([{ id: "1", label: "오늘" }, { id: "3", label: "최근 3일" }, { id: "5", label: "최근 5일" }], rotPeriod, "data-rp") +
      (list.length ? list.map(function (t, i) {
        return '<details class="rotrow"><summary><span class="shrank">' + (i + 1) + '</span><span class="rn">' + esc(t.name) + "</span>" +
          '<span class="rv"><b class="' + (t.ret > 0 ? "up" : "down") + '">' + sgn(t.ret) + '</b><span class="meta">거래대금 ' + t.ratio.toFixed(1) + "배 · " + won억(t.amt) + "</span></span></summary>" +
          '<div class="uschips">' + (t.stocks || []).map(function (s) {
            return '<a class="uschip" style="background:' + heatColor(s.pct, 10) + '" href="https://m.stock.naver.com/domestic/stock/' + encodeURIComponent(s.code) + '/total" target="_blank" rel="noopener noreferrer"><b>' +
              esc(s.name) + "</b> " + sgn(s.pct) + " · " + won억(s.amt) + "</a>";
          }).join("") + "</div></details>";
      }).join("") : '<div class="muted">조건에 맞는 테마가 없습니다.</div>') +
      '<div class="muted" style="margin-top:6px">오르면서 거래대금이 평소(직전 20일 평균)보다 늘어난 테마 순서입니다. 줄을 누르면 오늘 거래대금이 큰 종목이 보입니다.</div></div>';

    // 2) 날짜별 주도 테마
    h += '<div class="card"><h3>순환매 흐름 · 날짜별 주도 테마</h3>' + (R.daily || []).map(function (d) {
      return '<div class="rotday"><span class="rd">' + md(d.date) + "</span><div>" + (d.top.length ? d.top.map(function (t, i) {
        return '<span class="uschip" style="background:' + heatColor(t.ret, 6) + '">' + ["①", "②", "③"][i] + " <b>" + esc(t.name) + "</b> " + sgn(t.ret) + " · " + t.ratio.toFixed(1) + "배</span>";
      }).join("") : '<span class="meta">뚜렷한 주도 테마 없음</span>') + "</div></div>";
    }).join("") + '<div class="muted" style="margin-top:6px">그날 평균 +1% 이상 오르고 거래대금이 300억 원 이상인 테마 중, 등락률 × 거래대금 배수가 큰 순서 3개입니다.</div></div>';

    // 3) 히트맵
    if ((R.heat || []).length) {
      h += '<div class="card"><h3>주도 테마 일별 등락 (최근 ' + R.days.length + '거래일)</h3><div class="rotgrid" style="grid-template-columns:minmax(96px,1.6fr) repeat(' + R.days.length + ',1fr)">' +
        "<span></span>" + R.days.map(function (d) { return '<span class="rh">' + d.slice(8) + "</span>"; }).join("") +
        R.heat.map(function (t) {
          return '<span class="rname">' + esc(t.name) + "</span>" + t.rets.map(function (v, i) {
            return '<span class="rc' + (t.top[i] ? " top" : "") + '" style="background:' + heatColor(v, 6) + '" title="' + sgn(v) + '">' + (Math.abs(v) >= 10 ? v.toFixed(0) : v.toFixed(1)) + "</span>";
          }).join("");
        }).join("") + "</div>" +
        '<div class="muted" style="margin-top:6px">숫자는 테마 평균 등락률(%), 흰 테두리는 그날 주도 테마 3위 안에 든 날입니다. 진한 색이 왼쪽에서 오른쪽으로 옮겨 가는 모습이 순환매입니다.</div></div>';
    }

    // 4) 돈이 빠진 테마
    var out = (R.outflow || {})[rotPeriod] || [];
    if (out.length) {
      h += '<div class="card"><h3>돈이 빠진 테마</h3>' + out.map(function (t) {
        return '<div class="rotrow plain"><span class="rn">' + esc(t.name) + '</span><span class="rv"><b class="down">' + sgn(t.ret) + '</b><span class="meta">거래대금 ' + t.ratio.toFixed(1) + "배 · " + won억(t.amt) + "</span></span></div>";
      }).join("") + "</div>";
    }
    return h + '<div class="note">테마 분류와 구성종목은 네이버 증권 기준이고, 등락률은 구성종목의 단순 평균입니다. 외국인·기관 수급이 아니라 가격과 거래대금으로 본 자금 쏠림입니다.</div>';
  }

  function renderLive() {
    var root = $("#tab-live");
    var L = D.live || {};
    var m = L[liveMarket] || {};
    var h = sampleNote(L) + '<div class="live-head"><h2>실시간 특징주</h2>' +
      '<button type="button" class="refresh' + (liveStatus.indexOf("실패") === 0 ? " err" : "") + '" id="live-refresh"' + (liveBusy ? " disabled" : "") + '>' +
      (liveBusy ? "불러오는 중…" : "↻ 새로고침") + "</button></div>";
    h += '<div class="muted" style="margin-bottom:8px">데이터 기준 ' + esc(L.asOf || "-") + (liveStatus ? " · " + esc(liveStatus) : "") + "</div>";
    h += seg([{ id: "kr", label: "국내" }, { id: "us", label: "미국" }, { id: "rot", label: "테마 순환매" }], liveMarket, "data-lm");
    if (liveMarket === "rot") { root.innerHTML = h + rotationHtml(); return; }

    if (m.gainers) h += '<div class="card"><h3>등락률 상위</h3>' + rankBlock("gainers", m.gainers) + "</div>";
    if (m.value) {
      h += '<div class="card"><h3>거래대금 상위</h3>' + rankBlock("value", m.value, function (s) {
        return s.valueEok != null ? num(s.valueEok) + "억" : "";
      }) + "</div>";
    }

    if (m.themes) {
      h += '<div class="card"><h3>테마별 강약</h3><div class="note">' +
        '<span class="lg"><i style="background:var(--strong)"></i>강함 ' + (LIVE_STRONG > 0 ? "+" : "") + LIVE_STRONG + "% 이상</span>" +
        '<span class="lg"><i style="background:var(--weak)"></i>약함 ' + LIVE_WEAK + "% 이하</span></div>";
      m.themes.map(function (t) {
        var st = (t.stocks || []).slice().sort(function (a, b) { return b.changePct - a.changePct; });
        var avg = st.length ? st.reduce(function (a, s) { return a + (Number(s.changePct) || 0); }, 0) / st.length : 0;
        return { t: t, st: st, avg: t.rate != null ? Number(t.rate) : avg };
      }).sort(function (a, b) { return b.avg - a.avg; }).forEach(function (o) {
        h += '<div style="margin-bottom:12px"><div class="theme-head"><b>' + esc(o.t.name) + "</b>" + (o.t.total ? '<span class="meta"> 상승 ' + o.t.rise + "/" + o.t.total + "</span>" : "") + pctText(o.avg) + "</div>" +
          o.st.map(function (s) {
            return '<span class="sc ' + strengthClass(s.changePct) + '"><b>' + esc(s.name) + "</b> " + (Number(s.changePct) > 0 ? "+" : "") + (Number(s.changePct) || 0).toFixed(1) + "%</span>";
          }).join("") + "</div>";
      });
      if (!m.themes.length) h += '<div class="muted">테마 데이터가 없습니다.</div>';
      h += "</div>";
    }
    if (!m.gainers && !m.value && !m.themes) h += '<div class="card empty">이 시장은 아직 표시할 데이터가 없습니다.</div>';
    h += '<div class="note">새로고침은 서버에 저장된 최신 데이터를 다시 불러옵니다. 데이터 자체는 수집 주기마다 갱신되므로 위의 "데이터 기준" 시각을 확인하세요.</div>';
    root.innerHTML = h;
  }

  function reloadLive() {
    if (liveBusy) return;
    liveBusy = true; liveStatus = ""; renderLive();
    var old = document.getElementById("live-js");
    var sc = document.createElement("script");
    sc.id = "live-js";
    sc.src = "data/live.js?t=" + Date.now();   // 주소 뒤에 시각을 붙여 항상 최신 파일을 받는다
    sc.onload = function () { liveBusy = false; liveStatus = "새로고침 " + new Date().toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit", second: "2-digit" }); renderLive(); };
    sc.onerror = function () { liveBusy = false; liveStatus = "실패: 데이터를 불러오지 못했습니다"; renderLive(); };
    if (old && old.parentNode) old.parentNode.removeChild(old);
    document.body.appendChild(sc);
  }

  function initLive() {
    renderLive();
    $("#tab-live").addEventListener("click", function (ev) {
      if (ev.target.closest("#live-refresh")) { reloadLive(); return; }
      var mb = ev.target.closest("[data-more]");
      if (mb) { var k = mb.getAttribute("data-more") + liveMarket; liveMore[k] = !liveMore[k]; renderLive(); return; }
      var b = ev.target.closest("[data-lm]");
      var rp = ev.target.closest("[data-rp]");
      if (rp) { rotPeriod = rp.getAttribute("data-rp"); renderLive(); return; }
      if (b) { liveMarket = b.getAttribute("data-lm"); renderLive(); }
    });
  }

  /* ---------- 3장: 유튜브 ---------- */
  function renderYouTube() {
    var root = $("#tab-youtube");
    var y = D.youtube || {};
    var hasAI = (y.channels || []).some(function (c) { return (c.videos || []).some(function (v) { return v.ai && v.ai.keySummary; }); });
    var h = sampleNote(y) + "<h2>유튜브 최신 영상</h2>" +
      '<div class="muted">' + (hasAI ? "AI(제미나이)가 영상을 보고 정리한 요약입니다. 참고용이니 중요한 내용은 원본 영상으로 확인하세요." : "채널별 최신 영상 목록입니다. ‘재미나이로 요약’을 누르면 요청문이 복사되고 재미나이가 열립니다. 입력창에 붙여넣기만 하세요.") + "</div>" +
      (y.asOf ? '<div class="muted">목록 기준 ' + esc(y.asOf) + "</div>" : "") +
      (hasAI && (y.aiStatus || []).length ? '<div class="muted">AI 요약 상태: ' + y.aiStatus.map(esc).join(" / ") + "</div>" : "");

    // 여러 채널이 같이 언급한 종목 (최근 요약 기준)
    var mention = {};
    (y.channels || []).forEach(function (c) {
      (c.videos || []).forEach(function (v) {
        if (!v.ai || !v.ai.sectors) return;
        v.ai.sectors.forEach(function (s) { (s.stocks || []).forEach(function (st) {
          mention[st.name] = mention[st.name] || {};
          mention[st.name][c.name] = true;
        }); });
      });
    });
    var multi = Object.keys(mention).filter(function (k) { return Object.keys(mention[k]).length >= 2; });
    if (multi.length) {
      h += '<div class="card"><h3>여러 채널이 함께 언급한 종목</h3>' + multi.map(function (k) {
        return '<div class="stock"><span class="nm">' + esc(k) + '</span> <span class="muted">' + esc(Object.keys(mention[k]).join(" · ")) + "</span></div>";
      }).join("") + "</div>";
    }

    (y.channels || []).forEach(function (c, ci) {
      var vs = c.videos || [];
      h += '<div class="card"><h3>' + esc(c.name) + "</h3>";
      if (!vs.length) h += '<div class="muted">아직 수집된 영상이 없습니다. 자동 갱신 후 표시됩니다.</div>';
      vs.forEach(function (v, vi) {
        var ai = v.ai && v.ai.keySummary ? v.ai : null;
        h += '<div class="stock"><div class="nm">' + esc(v.title) + "</div>" +
          '<div class="meta">' + esc(v.publishedAt) + ' · <a href="' + esc(safeUrl(v.url)) + '" target="_blank" rel="noopener noreferrer">영상 보기</a>' +
          (ai ? "" : ' · <a href="#" class="gem" data-c="' + ci + '" data-v="' + vi + '">재미나이로 요약</a>') + "</div>";
        if (ai) {
          h += '<div class="keysum">' + esc(ai.keySummary) + "</div>";
          var det = "";
          if ((ai.market || []).length) det += "<h4>시장·거시</h4><ul class='plain'>" + ai.market.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul>";
          (ai.sectors || []).forEach(function (s) {
            det += "<h4>" + esc(s.name) + "</h4>" + (s.point ? "<div>" + esc(s.point) + "</div>" : "") +
              (s.stocks || []).map(function (st) { return '<div class="muted">· <b>' + esc(st.name) + "</b> " + esc(st.note) + "</div>"; }).join("");
          });
          if ((ai.checkpoints || []).length) det += "<h4>체크포인트</h4><ul class='plain'>" + ai.checkpoints.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul>";
          if (det) h += "<details><summary>상세 리포트 펼치기</summary>" + det + "</details>";
        }
        h += "</div>";
      });
      if (c.handle) h += '<a class="btnlink" href="https://www.youtube.com/' + encodeURI(c.handle) + '/videos" target="_blank" rel="noopener noreferrer">채널 영상 전체 보기 ›</a>';
      h += "</div>";
    });
    root.innerHTML = h;
    root.onclick = function (ev) {
      var a = ev.target.closest("a.gem");
      if (!a) return;
      ev.preventDefault();
      var v = y.channels[+a.getAttribute("data-c")].videos[+a.getAttribute("data-v")];
      var text = "다음 유튜브 영상을 한국어로 요약해줘. 핵심 3~5줄, 언급된 종목·수치·전망 위주로.\n" + v.url;
      var done = function () { window.open("https://gemini.google.com/app", "_blank", "noopener"); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () { window.prompt("복사해서 재미나이에 붙여넣으세요", text); done(); });
      else { window.prompt("복사해서 재미나이에 붙여넣으세요", text); done(); }
    };
  }

  /* ---------- 공통: 종목 카드 (4장·5장) ---------- */
  var LETTER = ["a", "b", "c", "d", "e", "f", "g", "h"];
  function won억(v) {
    var n = Number(v) || 0;
    if (!n) return "-";
    return n >= 10000 ? (n / 10000).toFixed(n >= 100000 ? 0 : 1).replace(/\.0$/, "") + "조" : num(n) + "억";
  }
  /* 스캔 결과(일봉 기준) 위에 장중 현재가(quotes.js)를 덮어쓴다. asOf: 그 스캔의 기준일 */
  function withQuote(s, asOf) {
    var Q = D.quotes || {};
    var q = (Q.kr || {})[s.code];
    var o = {};
    for (var k in s) o[k] = s[k];
    o.priceLabel = "종가";
    if (!q) return o;
    if (!o.market) o.market = q.market;
    if (!o.marcap && q.marcap) o.marcap = q.marcap;
    if (!o.sector && q.sector) o.sector = q.sector;
    // 네이버 화면과 같은 값(전일종가·현재가·등락률)을 그대로 쓴다. 스캔 기준일보다 오래된 시세는 쓰지 않는다
    if (q.prev && String(q.day || "") >= String(asOf || "").slice(0, 10)) {
      o.prevClose = q.prev; o.close = q.price; o.changePct = q.pct; o.value = q.value;
      if (q.marcap) o.marcap = q.marcap;
      o.priceLabel = "현재가";
    }
    return o;
  }
  function stockCard(s, tags, isKR, priceLabel) {
    var code = s.code || "";
    var link = isKR ? "https://m.stock.naver.com/domestic/stock/" + encodeURIComponent(code) + "/chart"
                    : "https://finance.yahoo.com/chart/" + encodeURIComponent(code);
    var h = '<div class="stock"><div class="row"><div><span class="nm">' + esc(s.name) + '</span> ' +
      '<a class="chartlink" href="' + link + '" target="_blank" rel="noopener noreferrer" title="차트 보기">📈</a> ' +
      '<span class="meta">' + esc(code) + "</span></div></div>";
    if ((tags || []).length) h += '<div class="tagrow">' + tags.map(function (t) {
      return '<span class="rlabel rl-' + t.k + '">' + esc(t.title || t.text) + "</span>";
    }).join("") + "</div>";
    var chips = "";
    if (s.market) chips += '<span class="chip mk-' + esc(s.market.toLowerCase()) + '">' + esc(s.market) + "</span>";
    if (s.krRank) chips += '<span class="chip krr">🇰🇷 ' + esc(s.krRank) + "</span>";
    (s.themes || []).forEach(function (t) { chips += '<span class="chip thm">🔥 ' + esc(t) + "</span>"; });
    if (s.sector && s.sector !== "기타") chips += '<span class="chip">' + esc(s.sector) + "</span>";
    if (chips) h += "<div>" + chips + "</div>";
    var pc = Number(s.changePct);
    var dir = s.changePct == null ? "flat" : pc > 0 ? "up" : pc < 0 ? "down" : "flat";
    h += '<div class="pricerow">' +
      (s.prevClose ? '<span class="lbl">전일종가</span> <span class="blk">' + num(s.prevClose) + '</span><span class="arrow">→</span>' : "") +
      '<span class="lbl">' + (priceLabel || "현재가") + '</span> <b class="' + dir + '">' + num(s.close) + "</b>" +
      (s.changePct != null ? ' <b class="' + dir + ' pct">' + (pc > 0 ? "▲ +" : pc < 0 ? "▼ " : "") + pc.toFixed(2) + "%</b>" : "") + "</div>";
    var ex = [];
    if (s.marcap) ex.push("시총 " + won억(s.marcap));
    if (s.value) ex.push("거래대금 " + won억(s.value));
    if (ex.length) h += '<div class="meta">' + ex.join(" · ") + "</div>";
    return h;
  }

  /* ---------- 4장: 중장기 ---------- */
  function renderLong() {
    var root = $("#tab-long");
    var L = D.longterm || {};
    var market = "kr";
    var view = "swing";      // swing = 스윙 투자, long = 중장기 투자
    try { view = sessionStorage.getItem("longView") || "swing"; } catch (e) {}
    var maText = function (v) { return v ? num(v) : "-"; };

    function draw() {
      var isSwing = view === "swing";
      var rules = (isSwing ? L.swingRules : L.rules) || [];
      var letters = isSwing ? LETTER.map(function (x) { return x.toUpperCase(); }) : LETTER;
      var ruleLabel = {};
      var ruleIds = rules.map(function (r) { return r.id; });
      rules.forEach(function (r) { ruleLabel[r.id] = r.label; });
      var h = seg([{ id: "swing", label: "① 스윙 투자" }, { id: "long", label: "② 중장기 투자" }], view, "data-vw");
      h += "<h2>" + (isSwing ? "스윙 투자" : "중장기 투자") + "</h2>";
      h += '<div class="card"><h3>적용 규칙</h3><ul class="plain">' +
        rules.map(function (r, i) { return '<li><span class="rtag rt-' + i + '">' + letters[i] + "</span> <b>" + esc(r.label) + "</b> — " + esc(r.desc) + "</li>"; }).join("") + "</ul></div>";
      h += seg([{ id: "kr", label: "국내" }, { id: "us", label: "미국" }], market, "data-mk");
      var info = (L.scanInfo || {})[market];
      var items = (isSwing ? (L.swing || {})[market] : L[market]) || [];
      if (info && info.scanned) {
        h += '<div class="muted" style="margin:-4px 0 8px">기준일 ' + esc(info.asOf) + " · " + num(info.scanned) + "개 종목 스캔 · " + items.length + "개 충족" +
          (market === "kr" && D.quotes && D.quotes.asOf ? " · 현재가 " + esc(D.quotes.asOf) : "") + "</div>";
      }
      if (L.scanInfo && !(info && info.scanned)) {
        h += '<div class="card empty">아직 이 시장의 스캔 결과가 없습니다.</div>';
      } else if (isSwing && !L.swing) {
        h += '<div class="card empty">스윙 스캔 결과가 아직 없습니다. 다음 장 마감 스캔부터 채워집니다.</div>';
      } else if (!items.length) {
        h += '<div class="card empty">조건을 충족한 종목이 없습니다.</div>';
      } else {
        // 규칙별 개수 (눌러서 걸러 보기)
        var cnt = {};
        items.forEach(function (s) { (s.matched || []).forEach(function (m) { cnt[m] = (cnt[m] || 0) + 1; }); });
        h += '<div class="rulefilter">' + ['<button type="button" data-rf="" class="' + (!filter ? "on" : "") + '">전체 ' + items.length + "</button>"].concat(
          rules.map(function (r, i) {
            return '<button type="button" data-rf="' + esc(r.id) + '" class="' + (filter === r.id ? "on" : "") + '"><span class="rtag rt-' + i + '">' + letters[i] + "</span> " + (cnt[r.id] || 0) + "</button>";
          })).join("") + "</div>";
        var shown = filter ? items.filter(function (s) { return (s.matched || []).indexOf(filter) >= 0; }) : items;
        h += shown.length ? '<div class="card">' + shown.map(function (s) {
          var tags = (s.matched || []).map(function (m) {
            var i = Math.max(0, ruleIds.indexOf(m));
            return { k: i, text: letters[i] || "?", title: ruleLabel[m] || m };
          });
          var v = market === "kr" ? withQuote(s, info && info.asOf) : s;
          return stockCard(v, tags, market === "kr", v.priceLabel || "종가") +
            '<div class="meta">' + (isSwing ? "10일선 " + maText(s.ma10) + " · 20일선 " + maText(s.ma20) + " · 60일선 " + maText(s.ma60)
                                            : "240일선 " + maText(s.ma240) + " · 480일선 " + maText(s.ma480)) + "</div>" +
            (s.note ? '<div class="meta">' + esc(s.note) + "</div>" : "") + "</div>";
        }).join("") + "</div>" : '<div class="card empty">이 규칙에 해당하는 종목이 없습니다.</div>';
      }
      root.innerHTML = h;
    }
    var filter = "";
    root.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-mk]"), v = ev.target.closest("[data-vw]"), f = ev.target.closest("[data-rf]");
      if (v) { view = v.getAttribute("data-vw"); filter = ""; try { sessionStorage.setItem("longView", view); } catch (e) {} draw(); }
      else if (b) { market = b.getAttribute("data-mk"); filter = ""; draw(); }
      else if (f) { filter = f.getAttribute("data-rf"); draw(); }
    });
    draw();
  }

  /* ---------- 5장: 단기 (유형 A 종가배팅주: 세부 A1·A2·A3, 각 5종목) ---------- */
  function renderShort() {
    var root = $("#tab-short");
    var S = D.shortterm || {};
    var types = S.types || [];
    var typeId = types.length ? types[0].id : "";
    var sub = "";

    function draw() {
      var t = types.filter(function (x) { return x.id === typeId; })[0];
      var h = sampleNote(S) + "<h2>단기 트레이딩</h2>";
      h += seg(types.map(function (x) { return { id: x.id, label: x.id + " " + (x.name || "") }; }), typeId, "data-ty");
      if (!t) {
        h += '<div class="card empty">등록된 유형이 없습니다.</div>';
        root.innerHTML = h; return;
      }
      h += '<div class="card"><div class="row"><h3>' + esc(t.name) + '</h3><span class="chip">' + esc(t.timeframe) + "</span></div>" +
        (t.desc ? '<div class="muted">' + esc(t.desc) + "</div>" : "") +
        (t.id === "A"
          ? '<div class="muted">확인 시간대 ' + esc(S.window || "") + " · 갱신 " + esc(S.asOf || "-") + "</div>" +
            (S.phase ? '<div class="phase' + (S.flowConfirmed ? " ok" : "") + '">' + esc(S.phase) + "</div>" : "") +
            (S.status ? '<div class="muted">' + esc(S.status) + "</div>" : "")
          : '<div class="muted">기준일 ' + esc(t.asOf || "-") + " (종가 기준)</div>") + "</div>";
      cur_asof = t.asOf || "";
      var subs = t.subtypes || [];
      if (subs.length) {
        if (!sub || !subs.some(function (x) { return x.id === sub; })) sub = subs[0].id;
        h += '<div class="seg">' + subs.map(function (x, i) {
          return '<button type="button" data-sb="' + esc(x.id) + '" class="' + (x.id === sub ? "on" : "") + '"><span class="rtag rt-' + i + '">' + esc(x.id) + "</span></button>";
        }).join("") + "</div>";
        var cur = subs.filter(function (x) { return x.id === sub; })[0];
        h += '<div class="card"><h3>' + esc(cur.name) + '</h3><div class="muted">' + esc(cur.desc || "") + "</div></div>";
        var items = cur.kr || [];
        if (!items.length) h += '<div class="card empty">지금 조건을 충족한 종목이 없습니다.</div>';
        else h += '<div class="card">' + items.map(function (s) { return stockRow(s, cur.id, subs.indexOf(cur), cur.short || cur.name); }).join("") + "</div>";
      } else {
        var its = t.kr || [];
        h += its.length ? '<div class="card">' + its.map(function (s) { return stockRow(s, "", 0); }).join("") + "</div>" : '<div class="card empty">조건을 충족한 종목이 없습니다.</div>';
      }
      root.innerHTML = h;
    }
    var cur_asof = "";
    function stockRow(s, id, i, subName) {
      var af = s.after && Math.abs(s.after.price - s.close) > 1e-9 ? s.after : null;
      var isB = String(id).charAt(0) === "B";
      if (isB) s = withQuote(s, cur_asof);      // 유형 B 는 일봉(종가) 기준이라 장중에는 현재가를 덧씌운다
      return stockCard(s, id ? [{ k: i, text: id, title: (subName || "") }] : [], true, isB ? (s.priceLabel || "종가") : (s.after ? "종가" : "현재가")) +
        (af ? '<div class="meta">마감 후 현재가(시간외) <b class="' + (af.pct > 0 ? "up" : af.pct < 0 ? "down" : "flat") + '">' + num(af.price) + " " +
          (af.pct > 0 ? "+" : "") + af.pct.toFixed(2) + "%</b></div>" : "") +
        (s.note ? '<div class="meta">' + esc(s.note) + "</div>" : "") + "</div>";
    }
    root.addEventListener("click", function (ev) {
      var a = ev.target.closest("[data-ty]");
      var b = ev.target.closest("[data-sb]");
      if (a) { typeId = a.getAttribute("data-ty"); sub = ""; draw(); }
      else if (b) { sub = b.getAttribute("data-sb"); draw(); }
    });
    draw();
  }

  /* ---------- 탭 전환 (주소 뒤 #us 처럼 특정 탭으로 바로 열 수 있음) ---------- */
  var TABS = ["calendar", "us", "live", "youtube", "long", "short"];
  function show(name) {
    if (TABS.indexOf(name) < 0) name = "calendar";
    $$(".tab").forEach(function (t) { t.classList.toggle("active", t.id === "tab-" + name); });
    $$("#tabbar button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-tab") === name); });
    if (location.hash !== "#" + name) {
      try { history.replaceState(null, "", "#" + name); } catch (e) { location.hash = name; }
    }
    window.scrollTo(0, 0);
  }

  function init() {
    var meta = D.meta || {};
    if (meta.title) { $("#title").textContent = meta.title; document.title = meta.title; }
    $("#updated").textContent = meta.updatedAt ? "마지막 갱신 " + meta.updatedAt : "";
    $("#sample-banner").hidden = !meta.isSample;

    renderCalendar(); renderUS(); initLive(); renderYouTube(); renderLong(); renderShort();

    // 전체 새로고침: 페이지를 다시 열면 모든 데이터 파일을 최신본으로 받는다 (보고 있던 탭은 주소의 #탭 으로 유지)
    var loadedAt = meta.updatedAt || "", hiddenAt = 0;
    var btn = $("#refresh-all");
    function hasNew() { return !!(D.meta && D.meta.updatedAt && D.meta.updatedAt !== loadedAt); }
    function mark() {
      if (!btn || !hasNew()) return;
      btn.classList.add("new");
      btn.textContent = "↻ 새 데이터 받기";
      $("#updated").textContent = "마지막 갱신 " + loadedAt + " → 새 데이터 " + D.meta.updatedAt;
    }
    function checkMeta(then) {      // 작은 meta.js 만 다시 받아 서버에 새 데이터가 올라왔는지 확인
      var s = document.createElement("script");
      s.src = "data/meta.js?t=" + Date.now();
      s.onload = function () { s.parentNode && s.parentNode.removeChild(s); mark(); if (then) then(); };
      s.onerror = function () { s.parentNode && s.parentNode.removeChild(s); };
      document.body.appendChild(s);
    }
    if (btn) btn.addEventListener("click", function () { btn.disabled = true; btn.textContent = "불러오는 중…"; location.reload(); });
    setInterval(function () { if (!document.hidden) checkMeta(); }, 60000);
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) { hiddenAt = Date.now(); return; }
      var away = hiddenAt && Date.now() - hiddenAt > 120000;      // 2분 넘게 다른 앱에 있다가 돌아왔고
      checkMeta(function () { if (away && hasNew()) location.reload(); });   // 새 데이터가 있으면 자동으로 다시 연다
    });

    $("#tabbar").addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-tab]");
      if (b) show(b.getAttribute("data-tab"));
    });
    window.addEventListener("hashchange", function () { show(location.hash.replace("#", "")); });
    show(location.hash.replace("#", ""));
  }

  init();
})();
