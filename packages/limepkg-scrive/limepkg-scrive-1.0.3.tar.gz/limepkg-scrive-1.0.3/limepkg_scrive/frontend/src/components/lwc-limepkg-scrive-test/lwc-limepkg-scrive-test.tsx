import {
    LimeWebComponent,
    LimeWebComponentContext,
    LimeWebComponentPlatform,
    NotificationService,
    PlatformServiceName,
    LimeobjectsStateService
} from '@limetech/lime-web-components-interfaces';
import { Component, Element, h, Prop, State} from '@stencil/core';
import { Configs, CurrentLimeobject, Limeobjects} from '@limetech/lime-web-components-decorators';
import { ListItem, ListSeparator, ValidationStatus, Tab} from '@limetech/lime-elements';


@Component({
    tag: 'lwc-limepkg-scrive-test',
    shadow: true,
    styleUrl: 'lwc-limepkg-scrive-test.scss',
})
export class Test implements LimeWebComponent {

    @CurrentLimeobject()
    @State()
    private document : any = {}

    @Prop()
    public platform: LimeWebComponentPlatform;

    @Configs({})
    @State()
    private config : any = {}

    @Prop()
    public context: LimeWebComponentContext;

    @Element()
    public element: HTMLElement;

    @State()
    public includePerson = false;


    private goToScrive(id) {
        const host = this.config.limepkg_scrive.scriveHost
        window.open(`${host}/public/?limeDocId=${id}${ this.includePerson ? "&usePerson=true" : ""}`);
    }

    public render() {
        if (this.context.limetype !== 'document') {
            return;
        }

        return (
            <div>
                <limel-collapsible-section header="Sign with Scrive">
                    <limel-button
                        label={`Design Contract`}
                        outlined={true}
                        onClick={() =>
                            this.goToScrive(this.context.id)
                        }
                    />
                    <limel-checkbox
                        label="Add associated person as signing party"
                        id="fab"
                        checked={this.includePerson}
                        required={false}
                        onChange={() => this.includePerson = !this.includePerson}
                    />
                </limel-collapsible-section>
            </div>
        );
    }
}
