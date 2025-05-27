from flask import Flask, render_template, request, flash, url_for, redirect
from config import wait_for_redis
from flask_wtf import CSRFProtect
from app.forms import PositionsForm
from app.utils import calculate_profit
from datetime import datetime
import json
from dotenv import load_dotenv
import os
import logging

load_dotenv()
r = wait_for_redis()

app = Flask(__name__)
app.secret_key = os.getenv('WTF_SECRET_KEY')
csrf = CSRFProtect(app)


@app.route('/signals/', methods=['GET', 'POST'])
def signals():
    """
    Route for handling signal entries.

    GET: Displays the signal submission form and available signal sets.
    POST: Validates and processes the form submission to store a new position entry.

    Data handled:
        - Signal name (from form)
        - Category (from request form)
        - Amount, Entry, Close, Strategy (from WTForms)
        - Timestamp of entry

    On successful form submission:
        - Stores the entry as a JSON object in Redis list 'jornal'.
        - Displays a success flash message and redirects back to the same page.

    On failure:
        - Displays an error flash message.

    Returns:
        Rendered HTML template 'signals.html'.
    """
    form = PositionsForm()
    now = datetime.now()

    signal_sets = {
        'Divergence': r.smembers('Divergence'),
        'SMA Cross': r.smembers('SMA Cross'),
        'Fibonacci': r.smembers('Fibonacci'),
        'Ichimoku Cloud': r.smembers('Ichimoku Cloud')
    }

    if request.method == 'POST' and form.validate_on_submit():
        signal = request.form.get("signal")
        category = request.form.get("category")

        data = {
            "signal": signal,
            "amount": form.amount.data,
            "entry": form.entry.data,
            "close": form.close.data,
            "date":  now.strftime("%Y-%m-%d %H:%M"),
            "choice": form.strategy.data,
            "category": category
        }

        r.lpush('jornal', json.dumps(data))
        flash(f"Successfully added position for {signal} using strategy {data['choice']}.", "success")
        return redirect(url_for('signals'))

    elif request.method == 'POST':
        flash("Form submission failed. Please check your input.", "danger")

    return render_template('signals.html', form=form, signal_sets=signal_sets)


@app.route('/jornal/')
def positions():
    """
    Route to display journaled trade positions.

    Supports filtering by:
        - Strategy (via 'strategy' query parameter)
        - Date (via 'date' query parameter)

    For each valid entry:
        - Parses the JSON data
        - Filters based on query params
        - Calculates profit using a utility function
        - Adds parsed data to a list to be rendered

    Total profit is aggregated and passed to the template.

    Returns:
        Rendered HTML template 'jornal.html'.
    """
    strategy_filter = request.args.get('strategy')
    date_filter = request.args.get('date')

    trades = r.lrange('jornal', 0, -1)
    parsed_trades = []
    total_profit = 0.0

    for trade in trades:
        try:
            data = json.loads(trade)

            if strategy_filter and data.get('choice') != strategy_filter:
                continue
            if date_filter and not data.get('date', '').startswith(date_filter):
                continue

            profit = calculate_profit(data['entry'], data['close'], data['choice'])
            data['profit'] = profit
            parsed_trades.append(data)
            total_profit += profit
        except (ValueError, KeyError, json.JSONDecodeError):
            logging.error('Error parsing trade')
            continue

    return render_template('jornal.html', trades=parsed_trades, total_profit=total_profit,
                           strategy_filter=strategy_filter, date_filter=date_filter)


@app.route('/jornal/delete/<int:index>', methods=['POST'])
def delete_position(index):
    """
    Route to delete a position from the journal.

    Accepts:
        - index (int): Index of the trade in the Redis list to be deleted.

    Behavior:
        - Fetches all trades from Redis list 'jornal'
        - If index is within bounds, removes the item at that position
        - Redirects to the journal page

    Returns:
        Redirect response to '/jornal/'.
    """
    trades = r.lrange('jornal', 0, -1)
    if 0 <= index < len(trades):
        r.lrem('jornal', 1, trades[index])
    return redirect(url_for('positions'))
