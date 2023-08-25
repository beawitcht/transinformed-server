from flask import Blueprint, render_template, abort, redirect, request
from pathlib import Path
from main import cache
from forms.checkout_forms import PurchaseForm, UploadForm
from werkzeug.utils import secure_filename
import stripe
import os

site_url = os.getenv('SITE_URL')
stripe.api_key = os.getenv('STRIPE_KEY')
stripe_endpoint_secret = os.getenv('STRIPE_EP_SEC')

checkout_bp = Blueprint('checkout', __name__)

customer_docs_path = Path(__file__).parent.parent / 'customer_docs'

def verify_purchased(session_id):
    checkout_session = stripe.checkout.Session.retrieve(session_id)

    payment_intent = stripe.PaymentIntent.retrieve(checkout_session.payment_intent)
    if payment_intent.status != "succeeded":
        return False, 402

    if checkout_session and checkout_session['mode'] == 'payment':
        return True, 200
    
    return False, 402

@checkout_bp.route("/checkout", methods=['GET', 'POST'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def checkout():
    form = PurchaseForm()
    if form.validate_on_submit():
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NiFmFDxqCcywEZnprv4rtLc',
                        'quantity': 1,
                    },
                ],
                phone_number_collection={
                    'enabled': True,
                },
                shipping_address_collection={
                    'allowed_countries': ['GB']
                },
                mode='payment',
                success_url= site_url + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url= site_url + '/',
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)


    return render_template("checkout.html", form=form)

@checkout_bp.route("/success", methods=['GET', 'POST'])
def success():
    form = UploadForm()

    if request.method == "POST":
        session_id = form.id.data

        if not session_id:
            return abort(400)

    if request.method == "GET":

        session_id = request.args.get('session_id')
        
        if not session_id:
            return abort(400)
    
        form.id.data = session_id

    if form.validate_on_submit():
        filename = secure_filename(form.upload.data.filename)
        id = secure_filename(form.id.data)
        if ".docx" == filename[-5:]:
            form.upload.data.save(os.path.join(customer_docs_path, id + ".docx"))
        elif ".pdf" == filename[-4:]:
            form.upload.data.save(os.path.join(customer_docs_path, id + ".pdf"))
        else:
            abort(415)

        return render_template("success.html", form=form, session_id=session_id, uploaded=True, site_url=site_url)
    
    try:
        # Check the session with stripe - this is not robust but for our purposes good enough, each payment will be manually verified
        verified = verify_purchased(session_id)
        if verified[0]:
            # Payment is verified
            return render_template("success.html", form=form, session_id=session_id, site_url=site_url)
        else:
            abort(verified[1])
    
    except stripe.error.StripeError:
        abort(498)

    
    
@checkout_bp.route("/cancel", methods=['GET'])
def cancel():
    return render_template("cancel.html")

@checkout_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NiFmFDxqCcywEZnprv4rtLc',
                    'quantity': 1,
                },
            ],
            phone_number_collection={
                'enabled': True,
            },
            shipping_address_collection={
                'allowed_countries': ['GB']
            },
            mode='payment',
            success_url= site_url + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url= site_url + '/',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

# @checkout_bp.route('/upload-document', methods=['POST'])
# def upload_document():
