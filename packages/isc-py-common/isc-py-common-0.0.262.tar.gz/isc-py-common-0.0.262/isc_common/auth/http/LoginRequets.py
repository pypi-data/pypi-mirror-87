import logging
import time
import uuid
from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from history.models.visitor import Visitor
from history.utils import get_ip
from isc_common import setAttr
from isc_common.auth.models.user import User
from isc_common.bit import IsBitOn, TurnBitOn, TurnBitOff
from isc_common.datetime import DateToStr
from isc_common.http.DSRequest import DSRequest
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.ws.webSocket import WebSocket
from tracker.models.messages_state import Messages_state
from tracker.models.messages_theme import Messages_theme
from twits.models.chat_user_user import Chat_user_user
from twits.models.chat_user_user_theme import Chat_user_user_theme
from twits.models.chat_users_view import Chat_usersView

logger = logging.getLogger(__name__)


class LoginRequest(DSRequest):
    def __init__(self, request):
        from django.forms import model_to_dict
        from kaf_pas.planing.models.status_operation_types import Status_operation_types
        from reports.models.jasper_reports_users import Jasper_reports_users
        from kaf_pas.planing.models.production_order import Production_orderQuerySet

        DSRequest.__init__(self, request)
        data = self.get_data()
        login = data.get('login', None)
        errorMessage = "Аутентификация не прошла :-("

        try:
            user = User.objects.get(username=login)

            if user.check_password(data.get('password', None)):
                ws_channel = f'{settings.WS_CHANNEL}_{login}'

                ip = get_ip(request)

                with transaction.atomic():
                    Visitor.objects.using('history').select_for_update()
                    # visitors_all = [visitor for visitor in Visitor.objects.using('history').filter(username=login)]
                    # if len(visitors_all) > 1:
                    #     Visitor.objects.using('history').filter(username=login).delete()

                    if settings.FREQUENCY_OF_POLLING_UNREAD_MESSAGES is None:
                        settings.FREQUENCY_OF_POLLING_UNREAD_MESSAGES = 1000 * 60 * 3

                    visitors = [visitor.ip_address for visitor in Visitor.objects.using('history').filter(username=login).exclude(ip_address=ip)]
                    if len(visitors) > 0:
                        ip_address = visitors[0]
                        if ip_address != ip:
                            self.response = dict(status=RPCResponseConstant.statusLoginIncorrect, errorMessage=f'Вход с логином "{login}" уже выполнен на {ip_address}')
                    else:

                        operations_statuses = []

                        for status_operation_types in Status_operation_types.objects.all():
                            operations_statuses.append(
                                dict(
                                    opertype_id=status_operation_types.opertype.id,
                                    opertype__code=status_operation_types.opertype.code,
                                    status_id=status_operation_types.id,
                                    status__code=status_operation_types.code,
                                    status__name=status_operation_types.name,
                                ))

                        from kaf_pas.ckk.models.locations_users import Locations_users
                        from kaf_pas.ckk.models.locations_view import Locations_view
                        if user.is_admin or user.is_develop:
                            workshops = []
                        else:
                            workshops = [Locations_view.objects.get(id=Locations_users.location.id).workshop for Locations_users in Locations_users.objects.filter(user=user)]
                            workshops = [workshop.id if workshop else 0 for workshop in workshops]
                            if len(workshops) == 0:
                                workshops = [-1]

                        location_ids = Production_orderQuerySet.get_user_locations(user=user)
                        self.response = dict(
                            # progresses=[ProgressesManager.getRecord(item) for item in Progresses.objects.filter(user=user)],
                            captionUser=user.get_short_name,
                            chatInfo=LoginRequest.get_chats(user),
                            CKK_CONFIGURATOR=settings.CKK_CONFIGURATOR,
                            codeGroup="",
                            DEFAULT_TIMEOUT=settings.DEFAULT_TIMEOUT,
                            dynDataSources=settings.DYNAMIC_CLASS.get_datasources(),
                            ENABLE_FILE_VIEW=settings.ENABLE_FILE_VIEW,
                            fio=user.get_short_name,
                            frequencyOfPollingUnreadMessages=settings.FREQUENCY_OF_POLLING_UNREAD_MESSAGES,
                            isAdmin=user.is_admin,
                            isDevelop=user.is_develop,
                            jsLogDebug=settings.JS_LOG_DEBUG if settings.JS_LOG_DEBUG == 1 else 0,
                            KOMPAS_INFORMICA=settings.KOMPAS_INFORMICA,
                            KOMPAS_INFORMICA_WS=settings.KOMPAS_INFORMICA_WS,
                            location_ids=location_ids,
                            location_ids_suffix='_'.join(map(lambda x: str(x), location_ids)) if location_ids is not None else None,
                            login=login,
                            message_state_delivered_id=Messages_state.message_state_delivered().id,
                            message_state_delivered_name=Messages_state.message_state_delivered().name,
                            message_state_new_id=Messages_state.message_state_new().id,
                            message_state_new_name=Messages_state.message_state_new().name,
                            message_state_not_readed_id=Messages_state.message_state_not_readed().id,
                            message_state_not_readed_name=Messages_state.message_state_not_readed().name,
                            message_state_readed_id=Messages_state.message_state_readed().id,
                            message_state_readed_name=Messages_state.message_state_readed().name,
                            Operations_Plan=settings.OPERATIONS_PLAN.OPERSTYPES,
                            operations_statuses=operations_statuses,
                            status=RPCResponseConstant.statusSuccess,
                            user__color=user.color if user.color is not None and user.color != 'undefined' else 'black',
                            user_full_name=user.get_full_name,
                            user_short_name=user.get_short_name,
                            userId=user.id,
                            username=user.username,
                            workshops=workshops,
                            ws_channel=ws_channel,
                            ws_host=settings.WS_HOST,
                            ws_port=settings.WS_PORT,
                            jasper_reports=[dict(
                                report=model_to_dict(item.report),
                                editor_identifier=item.editor_identifier,
                            ) for item in Jasper_reports_users.objects.filter(user=user)]
                        )
                        request.session['ws_channel'] = ws_channel
                        # request.session['ws_port'] = settings.WS_PORT
                        # request.session['host'] = settings.WS_HOST
                        # request.session['username'] = user.username
                        # request.session['fio'] = user.get_short_name
                        # request.session['user_id'] = user.id
                        # request.session['is_admin'] = user.is_admin
                        # request.session['is_develop'] = user.is_develop
                        user.last_login = datetime.now()
                        user.save()

            else:
                self.response = dict(status=RPCResponseConstant.statusLoginIncorrect, errorMessage=errorMessage)

        except User.DoesNotExist:
            self.response = dict(status=RPCResponseConstant.statusLoginIncorrect, errorMessage=errorMessage)

    @staticmethod
    def get_chats(user):
        tetatet_chats_reciver = []
        tetatet_chats_sender = []
        tetatet_chats = []

        key = 'LoginRequest.get_chats'
        settings.LOCKS.acquire(key)
        for chat in Chat_user_user.objects.filter(user_reciver=user):
            tetatet_chats_reciver.append(dict(
                id=chat.common_id,
                props=chat.props._value,
                sender_id=chat.user_sender.id,
                fullname=chat.user_sender.get_full_name,
                shortname=chat.user_sender.get_short_name,
                theme_ids=[item.theme.id for item in Chat_user_user_theme.objects.filter(chat_user_user__common_id=chat.common_id)],
                view_theme_ids=[item.theme.id for item in Chat_user_user_theme.objects.filter(chat_user_user__common_id=chat.common_id) if item.chat_user_user.user_sender == user],
                readonly=True
            ))

        for chat in Chat_user_user.objects.filter(user_sender=user):
            tetatet_chats_sender.append(dict(
                id=chat.common_id,
                props=chat.props._value,
                reciver_id=chat.user_reciver.id,
                fullname=chat.user_reciver.get_full_name,
                shortname=chat.user_reciver.get_short_name,
                theme_ids=[item.theme.id for item in Chat_user_user_theme.objects.filter(chat_user_user__common_id=chat.common_id)],
                view_theme_ids=[item.theme.id for item in Chat_user_user_theme.objects.filter(chat_user_user__common_id=chat.common_id) if item.chat_user_user.user_sender == user],
                readonly=False
            ))

        for chat in tetatet_chats_reciver:
            chat2 = [item for item in tetatet_chats_sender if item.get('id') == chat.get('id')]
            read_only = len(chat2) == 0
            if read_only:
                tetatet_chats.append(chat)
            else:
                compulsory_reading = IsBitOn(chat.get('props'), 0)
                if compulsory_reading:
                    props = TurnBitOn(chat2[0].get('props'), 0)
                else:
                    props = TurnBitOff(chat2[0].get('props'), 0)
                setAttr(chat2[0], 'props', props)
                tetatet_chats.append(chat2[0])

        for chat in tetatet_chats_sender:
            chat2 = [item for item in tetatet_chats if item.get('id') == chat.get('id')]
            if len(chat2) == 0:
                tetatet_chats.append(chat)

        group_chats = [
            dict(
                id=chat_users.chat.id,
                props=chat_users.props._value,
                code=chat_users.chat.code,
                name=chat_users.chat.name,
                readonly=chat_users.readonly,
                theme_ids=[
                    Messages_theme.objects.get_or_create(
                        code=f'group_{chat_users.chat.code}',
                        defaults=dict(
                            name=f'Чат: {chat_users.chat.name}',
                            creator=User.admin_user(),
                            editing=False,
                            deliting=False,
                            parent=Messages_theme.group_chats_theme(),
                            description='Группа создана автоматически'))[0].id
                ],
            ) for chat_users in Chat_usersView.objects.filter(user=user)]
        settings.LOCKS.release(key)

        return dict(
            group_chats=group_chats,
            tetatet_chats=tetatet_chats,
        )

    @staticmethod
    def send_bot_message(user, bot, message, compulsory_reading=False):
        _user = user
        _bot = bot

        key = 'LoginRequest.send_bot_message'
        settings.LOCKS.acquire(key)
        if not isinstance(_user, User) and isinstance(_user, int):
            _user = User.objects.get(id=_user)

        if not isinstance(_bot, User) and isinstance(_bot, int):
            _bot = User.objects.get(id=_bot)

        props = TurnBitOn(0, 0) if compulsory_reading else TurnBitOff(0, 0)
        chat_user_user, created = Chat_user_user.objects.get_or_create(
            user_sender=_bot,
            user_reciver=_user,
            defaults=dict(props=props)
        )

        def send():
            channel = f'tetatet_{chat_user_user.common_id}'

            _message = dict(
                channel=channel,
                date=DateToStr(timezone.now(), '%d.%m.%Y, %H:%M:%S', 3),
                guid=uuid.uuid4(),
                host=settings.WS_HOST,
                message=f'<pre>{message}</pre>',
                message_state_delivered_id=Messages_state.message_state_delivered().id,
                message_state_delivered_name=Messages_state.message_state_delivered().name,
                message_state_new_id=Messages_state.message_state_new().id,
                message_state_new_name=Messages_state.message_state_new().name,
                message_state_readed_id=Messages_state.message_state_readed().id,
                message_state_readed_name=Messages_state.message_state_readed().name,
                message_state_not_readed_id=Messages_state.message_state_not_readed().id,
                message_state_not_readed_name=Messages_state.message_state_not_readed().name,
                path='twit',
                port=settings.WS_PORT,
                props=0,
                theme_ids=[item.theme.id for item in Chat_user_user_theme.objects.filter(chat_user_user=chat_user_user)],
                type='message',
                user__color=_bot.color if _bot.color else 'black',
                user__full_name=_bot.get_full_name,
                user__short_name=_bot.get_short_name,
                user_id=_bot.id
            )

            WebSocket.send_message(
                host=settings.WS_HOST,
                port=settings.WS_PORT,
                channel=channel,
                message=_message,
                logger=logger
            )

        if created:
            from twits.models.chats import ChatsManager
            ChatsManager.refresh_chat_menu(user=_user, logger=logger)
            time.sleep(3)
            send()
        else:
            if chat_user_user.props._value != props:
                chat_user_user.props = props
                chat_user_user.save()

                from twits.models.chats import ChatsManager
                ChatsManager.refresh_chat_menu(user=_user, logger=logger)
                time.sleep(3)
            send()
        settings.LOCKS.release(key)
